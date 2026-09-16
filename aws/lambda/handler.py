"""ThermoVerse AWS Lambda handlers for website inquiries and CRM operations."""
from __future__ import annotations
import json, os, re, uuid
from datetime import datetime, timezone
import boto3

TABLE = boto3.resource("dynamodb").Table(os.environ["INQUIRIES_TABLE"])
ORIGIN = os.environ["ALLOWED_ORIGIN"]
EMAIL = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+$")
TYPES = {"Schedule an Energy Assessment (Services) (New)", "Apply for LATCHES POC Site Partnership", "Technology / Engineering Inquiry", "FACES Workforce Program Interest", "General Inquiry"}
OPTIONAL = ("organization", "role", "source", "language", "siteType", "location", "siteDescription", "currentProblem", "dataAvailable", "contactTime")

def reply(status, payload):
    return {"statusCode": status, "headers": {"content-type":"application/json; charset=utf-8", "access-control-allow-origin":ORIGIN, "access-control-allow-headers":"content-type,authorization"}, "body":json.dumps(payload)}
def clean(value, limit=3000): return str(value or "").strip()[:limit]
def read(event):
    try: value=json.loads(event.get("body") or "{}")
    except json.JSONDecodeError as error: raise ValueError("Invalid JSON.") from error
    if not isinstance(value, dict): raise ValueError("Request body must be an object.")
    return value
def timestamp(): return datetime.now(timezone.utc).isoformat(timespec="seconds")

def submit_inquiry(event, _context):
    try:
        data=read(event)
        if data.get("website"): return reply(201,{"ok":True})
        name,email=clean(data.get("name"),200),clean(data.get("email"),254)
        inquiry_type,message=clean(data.get("inquiryType"),160),clean(data.get("message"),5000)
        if not name or not EMAIL.match(email): raise ValueError("Name and a valid email are required.")
        if inquiry_type not in TYPES: raise ValueError("Select a valid inquiry type.")
        if not message: raise ValueError("Message is required.")
        now=timestamp(); item={"id":str(uuid.uuid4()),"createdAt":now,"updatedAt":now,"status":"new","internalNote":"","name":name,"email":email,"inquiryType":inquiry_type,"message":message,"marketing":bool(data.get("marketing"))}
        item.update({key:clean(data.get(key)) for key in OPTIONAL})
        TABLE.put_item(Item=item,ConditionExpression="attribute_not_exists(id)")
        return reply(201,{"ok":True,"id":item["id"]})
    except ValueError as error: return reply(400,{"error":str(error)})
    except Exception: return reply(500,{"error":"Unable to receive the inquiry. Please try again shortly."})

def list_inquiries(_event, _context):
    try:
        items=TABLE.scan().get("Items",[])
        return reply(200,{"items":sorted(items,key=lambda item:item.get("createdAt",""),reverse=True)})
    except Exception: return reply(500,{"error":"Unable to load inquiries."})

def update_inquiry(event, _context):
    try:
        record_id=(event.get("pathParameters") or {}).get("id","")
        if not re.fullmatch(r"[a-f0-9-]{36}",record_id): raise ValueError("Invalid inquiry identifier.")
        data=read(event); status,note=clean(data.get("status"),30),clean(data.get("internalNote"),5000)
        if status not in {"new","in_review","contacted","closed"}: raise ValueError("Invalid status.")
        result=TABLE.update_item(Key={"id":record_id},UpdateExpression="SET #s=:s, internalNote=:n, updatedAt=:u",ConditionExpression="attribute_exists(id)",ExpressionAttributeNames={"#s":"status"},ExpressionAttributeValues={":s":status,":n":note,":u":timestamp()},ReturnValues="ALL_NEW")
        return reply(200,{"ok":True,"item":result["Attributes"]})
    except ValueError as error: return reply(400,{"error":str(error)})
    except Exception: return reply(500,{"error":"Unable to update inquiry."})
