# AWS CRM 部署

`template.yaml` 是 ThermoVerse CRM 的 AWS SAM / CloudFormation 原始範本；它會建立 DynamoDB、Cognito、API Gateway 與 Lambda。公開網站的表單以 `POST /api/inquiries` 寫入，管理者端的讀取與狀態更新端點必須帶 Cognito JWT。

## 已完成的 AWS 狀態（2026-09-16）

- AWS IAM Identity Center SSO 已以帳號 `236934871408`、`WebDev` 角色完成設定。
- 私有部署桶 `thermoverse-aws-artifacts-236934871408` 已建立，且已啟用公開存取封鎖、S3 加密與版本控制。
- Lambda 部署封包已成功上傳。
- **CRM stack 尚未建立。** `WebDev` 缺少 `cloudformation:DescribeStacks`，AWS 在建立前即拒絕請求，沒有產生 DynamoDB、Cognito、API 或 Lambda 資源。

## 明天只需補一次的帳號設定

在 AWS Console 的 IAM Identity Center，替 `WebDev` permission set 加上 [`DEPLOYMENT_ACCESS_POLICY.json`](DEPLOYMENT_ACCESS_POLICY.json) 的權限（或讓有 CloudFormation 部署權的人套用此檔）。權限生效後，從專案根目錄執行：

```sh
/private/tmp/thermoverse-aws-cli/aws cloudformation deploy \
  --template-file /private/tmp/thermoverse-packaged.yaml \
  --stack-name thermoverse-crm-staging \
  --capabilities CAPABILITY_IAM \
  --parameter-overrides AllowedOrigin=https://YOUR-AMPLIFY-URL \
  --profile thermoverse --region us-east-1
```

部署完成後，將輸出的 `ApiBaseUrl` 放入 `website/config.js`：

```js
window.THERMO_API_BASE_URL = 'https://YOUR_API_ID.execute-api.us-east-1.amazonaws.com';
```

`website/config.js` 不會被 Git 追蹤；可從 `website/config.example.js` 複製。正式網域確定後，以正式 HTTPS origin 更新 `AllowedOrigin`，不可保留 localhost。

## CRM 前後端責任

- **公開前端**：`website/contact.html` 與 `website/zh/contact.html` 已將表單送至設定的 API URL；未設定 URL 時僅能配合本機 CRM 伺服器驗證。
- **API 後端**：`aws/lambda/handler.py` 執行欄位驗證、honeypot、防呆與 DynamoDB 寫入；管理 API 受 Cognito JWT 保護。
- **管理前端**：`crm/admin.html` 已實作詢問列表、狀態、內部備註與 CSV 匯出，現階段以本機 token 驗證。正式版在 Cognito stack 建成後替換登入流程，不會把管理 token 寫入靜態網站。

## 正式上線前保留的必要項目

- 先建立 Amplify Hosting，取得正式 HTTPS URL，再更新 CORS `AllowedOrigin`。
- 在 Cognito 建立 CRM 管理者帳號。
- 取得公司核定的隱私權、資料保存期限與行銷同意文案，才啟用行銷勾選。
- 若要寄新詢問通知，再驗證 SES 寄件身分與收件信箱；目前後端不寄信，因此不會誤寄。
