# ThermoVerse AWS IAM Role 說明與交付

更新日期：2026-09-16（臺灣時間）

這份文件把 `aws/template.yaml` 裡與 IAM Role 建立及授權有關的部分獨立整理，方便交給 AWS 管理員或同事審閱。

## 要交給同事的檔案

請將以下四個檔案一起交給同事：

1. [`aws/template.yaml`](template.yaml) —— 主要的 AWS SAM／CloudFormation 部署範本。
2. [`aws/lambda/handler.py`](lambda/handler.py) —— 範本引用的 Lambda 後端程式。
3. [`aws/DEPLOYMENT_ACCESS_POLICY.json`](DEPLOYMENT_ACCESS_POLICY.json) —— 給 `WebDev` Permission Set 使用的部署權限政策。
4. 本文件 —— IAM Role 與部署需求的說明。

`website/` 資料夾是前端，之後透過 Amplify Hosting 另外部署；同事建立 CRM 後端 stack 時不需要這個資料夾。

`template.yaml` 使用 AWS SAM 的 `CodeUri: lambda/`，要從專案資料夾用 SAM 部署，或先用 AWS CLI 打包。Lambda 程式碼上傳到 S3 前，不能直接當成完整檔案上傳到 CloudFormation Console。請不要交出 `crm/data/`、`website/config.js`、AWS access key、SSO token 或任何真實詢問資料。

Permission Set 更新後，建議使用：

```sh
sam build --template-file aws/template.yaml
sam deploy --guided --stack-name thermoverse-crm-staging
```

Stack 使用 `us-east-1`；出現 `AllowedOrigin` 時，填入 Amplify 完成部署後的正式 HTTPS 網址。

## 先說結論

原始的 CloudFormation 範本沒有手動寫死 `AWS::IAM::Role` 資源。它使用 AWS SAM 的 `AWS::Serverless::Function` 搭配 `Policies`；CloudFormation 在套用 SAM 轉換時，會替每個 Lambda 建立執行角色（execution role），再把指定的 DynamoDB 權限附加到該角色。

這個網站 CRM 需要三個 Lambda 執行角色：

| Lambda | 用途 | 角色需要的資料權限 |
|---|---|---|
| `SubmitInquiryFunction` | 接收公開表單、驗證欄位、寫入詢問 | DynamoDB 讀寫 `InquiriesTable` |
| `ListInquiriesFunction` | CRM 管理頁載入詢問 | DynamoDB 讀取 `InquiriesTable` |
| `UpdateInquiryFunction` | 更新狀態與內部備註 | DynamoDB 讀寫 `InquiriesTable` |

三個角色都由 CloudFormation 管理，不應由人工在 IAM 裡改角色名稱或信任政策。範本更新時，SAM 會同步更新角色與權限。

## 範本中實際涉及 Role 的片段

以下是從 `aws/template.yaml` 抽出的原始授權片段：

```yaml
SubmitInquiryFunction:
  Type: AWS::Serverless::Function
  Properties:
    Handler: handler.submit_inquiry
    Policies:
      - DynamoDBCrudPolicy:
          TableName: !Ref InquiriesTable

ListInquiriesFunction:
  Type: AWS::Serverless::Function
  Properties:
    Handler: handler.list_inquiries
    Policies:
      - DynamoDBReadPolicy:
          TableName: !Ref InquiriesTable

UpdateInquiryFunction:
  Type: AWS::Serverless::Function
  Properties:
    Handler: handler.update_inquiry
    Policies:
      - DynamoDBCrudPolicy:
          TableName: !Ref InquiriesTable
```

`DynamoDBCrudPolicy` 與 `DynamoDBReadPolicy` 是 SAM 的政策範本。它們會把 Lambda 限制在範本建立的 `InquiriesTable`，不會讓網站程式任意讀取整個 AWS 帳號的 DynamoDB 資料。

## 部署者本身需要的 IAM 權限

這部分是「部署者」的權限，不是 Lambda 執行角色的權限。CloudFormation 必須能建立 Lambda 執行角色並附加政策，因此部署者至少需要：

```text
iam:CreateRole
iam:GetRole
iam:DeleteRole
iam:AttachRolePolicy
iam:DetachRolePolicy
iam:PutRolePolicy
iam:DeleteRolePolicy
iam:PassRole
```

同時需要建立與更新 CloudFormation stack，以及建立 API Gateway、Lambda、DynamoDB 與 Cognito 資源的權限。完整的部署者政策仍放在：

`aws/DEPLOYMENT_ACCESS_POLICY.json`

其中 `iam:PassRole` 的意思是：允許 CloudFormation 把它建立的 Lambda 執行角色交給 Lambda 服務使用。它不等於把你的個人登入權限交給 Lambda。

## 給 AWS 管理員的處理方式

請在 IAM Identity Center 的 `WebDev` Permission Set 加入部署者政策，或建立一個暫時的 `ThermoVerseDeployment` Permission Set。不要直接修改 `AWSReservedSSO_WebDev_...` 角色；這類角色由 IAM Identity Center 管理。

如果公司先採用 AWS managed policies 讓部署完成，至少要確認：

- `AWSCloudFormationFullAccess`
- 能建立／更新 Lambda、DynamoDB、API Gateway 與 Cognito 的權限
- `iam:CreateRole`、`iam:AttachRolePolicy`、`iam:PutRolePolicy`、`iam:PassRole`
- 部署用 S3 bucket 的 `s3:GetObject`、`s3:PutObject`、`s3:ListBucket`

部署完成並驗證 staging 後，建議移除暫時的管理員級政策，改回 `aws/DEPLOYMENT_ACCESS_POLICY.json` 的範圍。

## 不應放進 Lambda Role 的權限

- 不需要 `AdministratorAccess` 作為 Lambda 執行角色權限。
- 不需要讓公開表單直接讀取 DynamoDB。
- 不需要把 Cognito 管理權限給公開表單 Lambda；Cognito 只用來保護 CRM 管理端點。
- 不要把 AWS access key、SSO token 或公司信箱寫入前端檔案。

## 來源與檢查結果

- 原始範本：`aws/template.yaml`
- Lambda 程式：`aws/lambda/handler.py`
- 部署者權限：`aws/DEPLOYMENT_ACCESS_POLICY.json`
- 目前 CloudFormation stack 尚未建立；本文件描述的是即將由 SAM 產生的 Role 與部署者需求，不代表 AWS 資源已存在。
