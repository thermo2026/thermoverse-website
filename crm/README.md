# 本機 CRM

此 CRM 可接收 ThermoVerse Contact Us 表單、以 SQLite 保存詢問，並提供管理者登入、狀態更新、內部備註與 CSV 匯出。

```sh
CRM_ADMIN_TOKEN='change-this-token' python3 crm/server.py
```

- 網站：`http://127.0.0.1:8787/`
- CRM：`http://127.0.0.1:8787/admin/`
- 資料庫：`crm/data/thermoverse-crm.sqlite3`（已列入 `.gitignore`）

預設 token 僅供本機開發：`local-development-only`。正式 AWS 不使用此登入方式，改用 Cognito；資料改存 DynamoDB，API contract 維持 `POST /api/inquiries`、`GET/PATCH /api/inquiries`。
