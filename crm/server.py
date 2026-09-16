#!/usr/bin/env python3
"""ThermoVerse local CRM and website server.

Run with: CRM_ADMIN_TOKEN='change-me' python3 crm/server.py
Open: http://127.0.0.1:8787/          (website)
      http://127.0.0.1:8787/admin/    (CRM)

This is intentionally dependency-free for local review. Production AWS uses the
same JSON contract behind API Gateway + Lambda + DynamoDB.
"""

from __future__ import annotations

import csv
import io
import json
import os
import re
import secrets
import sqlite3
import time
from datetime import datetime, timezone
from http import HTTPStatus
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent.parent
WEBSITE = ROOT / "website"
CRM_DIR = ROOT / "crm"
DATA_DIR = CRM_DIR / "data"
DB_PATH = DATA_DIR / "thermoverse-crm.sqlite3"
ADMIN_TOKEN = os.environ.get("CRM_ADMIN_TOKEN", "local-development-only")
MAX_BODY_BYTES = 24_000
RATE_WINDOW_SECONDS = 60
RATE_LIMIT = 12
RATE_LOG: dict[str, list[float]] = {}
EMAIL_RE = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+$")
ALLOWED_TYPES = {
    "Schedule an Energy Assessment (Services) (New)",
    "Apply for LATCHES POC Site Partnership",
    "Technology / Engineering Inquiry",
    "FACES Workforce Program Interest",
    "General Inquiry",
}
FIELDS = (
    "name", "email", "organization", "role", "inquiryType", "message", "source",
    "language", "siteType", "location", "siteDescription", "currentProblem",
    "dataAvailable", "contactTime", "marketing",
)


def db() -> sqlite3.Connection:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(DB_PATH)
    con.row_factory = sqlite3.Row
    con.execute("""
      CREATE TABLE IF NOT EXISTS inquiries (
        id TEXT PRIMARY KEY,
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL,
        status TEXT NOT NULL DEFAULT 'new',
        internal_note TEXT NOT NULL DEFAULT '',
        name TEXT NOT NULL, email TEXT NOT NULL, organization TEXT, role TEXT,
        inquiry_type TEXT NOT NULL, message TEXT NOT NULL, source TEXT, language TEXT,
        site_type TEXT, location TEXT, site_description TEXT, current_problem TEXT,
        data_available TEXT, contact_time TEXT, marketing INTEGER NOT NULL DEFAULT 0
      )
    """)
    con.commit()
    return con


def now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def clean(value: object, limit: int = 3000) -> str:
    return str(value or "").strip()[:limit]


class App(SimpleHTTPRequestHandler):
    server_version = "ThermoVerseCRM/1.0"

    def log_message(self, fmt: str, *args: object) -> None:
        print("[%s] %s" % (self.log_date_time_string(), fmt % args))

    def end_headers(self) -> None:
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("X-Frame-Options", "DENY")
        self.send_header("Referrer-Policy", "strict-origin-when-cross-origin")
        super().end_headers()

    def do_OPTIONS(self) -> None:
        self.send_response(HTTPStatus.NO_CONTENT)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, PATCH, OPTIONS")
        self.end_headers()

    def do_GET(self) -> None:
        path = urlparse(self.path).path
        if path == "/healthz":
            return self.json({"ok": True, "service": "thermoverse-crm"})
        if path == "/api/inquiries":
            return self.list_inquiries()
        if path == "/api/inquiries.csv":
            return self.export_csv()
        if path.startswith("/admin"):
            return self.serve_file(CRM_DIR / "admin.html", "text/html; charset=utf-8")
        return self.serve_website(path)

    def do_POST(self) -> None:
        if urlparse(self.path).path == "/api/inquiries":
            return self.create_inquiry()
        self.send_error(HTTPStatus.NOT_FOUND)

    def do_PATCH(self) -> None:
        match = re.fullmatch(r"/api/inquiries/([a-f0-9]{32})", urlparse(self.path).path)
        if match:
            return self.update_inquiry(match.group(1))
        self.send_error(HTTPStatus.NOT_FOUND)

    def serve_website(self, path: str) -> None:
        relative = path.lstrip("/") or "index.html"
        candidate = (WEBSITE / relative).resolve()
        if WEBSITE not in candidate.parents and candidate != WEBSITE:
            return self.send_error(HTTPStatus.NOT_FOUND)
        if candidate.is_dir():
            candidate /= "index.html"
        if not candidate.exists() or not candidate.is_file():
            return self.send_error(HTTPStatus.NOT_FOUND)
        mime = self.guess_type(str(candidate))
        self.serve_file(candidate, mime)

    def serve_file(self, file_path: Path, content_type: str) -> None:
        content = file_path.read_bytes()
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(content)))
        self.end_headers()
        self.wfile.write(content)

    def read_json(self) -> dict:
        length = int(self.headers.get("Content-Length", "0"))
        if length <= 0 or length > MAX_BODY_BYTES:
            raise ValueError("Invalid request size.")
        data = json.loads(self.rfile.read(length).decode("utf-8"))
        if not isinstance(data, dict):
            raise ValueError("Request body must be an object.")
        return data

    def json(self, data: object, status: HTTPStatus = HTTPStatus.OK) -> None:
        encoded = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(encoded)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(encoded)

    def is_rate_limited(self) -> bool:
        address = self.client_address[0]
        cutoff = time.time() - RATE_WINDOW_SECONDS
        recent = [stamp for stamp in RATE_LOG.get(address, []) if stamp > cutoff]
        RATE_LOG[address] = recent
        if len(recent) >= RATE_LIMIT:
            return True
        recent.append(time.time())
        return False

    def create_inquiry(self) -> None:
        try:
            payload = self.read_json()
            if payload.get("website"):
                return self.json({"ok": True}, HTTPStatus.CREATED)  # honeypot
            if self.is_rate_limited():
                return self.json({"error": "Please try again shortly."}, HTTPStatus.TOO_MANY_REQUESTS)
            item = {key: clean(payload.get(key)) for key in FIELDS}
            item["marketing"] = bool(payload.get("marketing"))
            if not item["name"] or not EMAIL_RE.match(item["email"]):
                raise ValueError("Name and a valid email are required.")
            if item["inquiryType"] not in ALLOWED_TYPES:
                raise ValueError("Select a valid inquiry type.")
            if not item["message"]:
                raise ValueError("Message is required.")
            identifier = secrets.token_hex(16)
            created = now()
            with db() as con:
                con.execute("""
                  INSERT INTO inquiries VALUES (?, ?, ?, 'new', '', ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (identifier, created, created, item["name"], item["email"], item["organization"], item["role"],
                      item["inquiryType"], item["message"], item["source"], item["language"], item["siteType"],
                      item["location"], item["siteDescription"], item["currentProblem"], item["dataAvailable"],
                      item["contactTime"], int(item["marketing"])))
            self.json({"ok": True, "id": identifier, "message": "Inquiry received."}, HTTPStatus.CREATED)
        except (ValueError, json.JSONDecodeError) as error:
            self.json({"error": str(error)}, HTTPStatus.BAD_REQUEST)

    def authorized(self) -> bool:
        value = self.headers.get("Authorization", "")
        return secrets.compare_digest(value, f"Bearer {ADMIN_TOKEN}")

    def require_admin(self) -> bool:
        if self.authorized():
            return True
        self.json({"error": "Administrator sign-in required."}, HTTPStatus.UNAUTHORIZED)
        return False

    def list_inquiries(self) -> None:
        if not self.require_admin():
            return
        with db() as con:
            rows = [dict(row) for row in con.execute("SELECT * FROM inquiries ORDER BY created_at DESC")]
        self.json({"items": rows})

    def update_inquiry(self, identifier: str) -> None:
        if not self.require_admin():
            return
        try:
            payload = self.read_json()
            status = clean(payload.get("status"), 30)
            note = clean(payload.get("internalNote"), 5000)
            if status not in {"new", "in_review", "contacted", "closed"}:
                raise ValueError("Invalid status.")
            with db() as con:
                cursor = con.execute("UPDATE inquiries SET status=?, internal_note=?, updated_at=? WHERE id=?", (status, note, now(), identifier))
            if not cursor.rowcount:
                return self.json({"error": "Inquiry not found."}, HTTPStatus.NOT_FOUND)
            self.json({"ok": True})
        except (ValueError, json.JSONDecodeError) as error:
            self.json({"error": str(error)}, HTTPStatus.BAD_REQUEST)

    def export_csv(self) -> None:
        if not self.require_admin():
            return
        with db() as con:
            rows = [dict(row) for row in con.execute("SELECT * FROM inquiries ORDER BY created_at DESC")]
        stream = io.StringIO()
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]) if rows else ["id", "created_at", "status", "name", "email"])
        writer.writeheader()
        writer.writerows(rows)
        encoded = stream.getvalue().encode("utf-8-sig")
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", "text/csv; charset=utf-8")
        self.send_header("Content-Disposition", "attachment; filename=thermoverse-inquiries.csv")
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        self.wfile.write(encoded)


if __name__ == "__main__":
    print("ThermoVerse CRM: http://127.0.0.1:8787/admin/")
    print("Website:          http://127.0.0.1:8787/")
    ThreadingHTTPServer(("127.0.0.1", 8787), App).serve_forever()
