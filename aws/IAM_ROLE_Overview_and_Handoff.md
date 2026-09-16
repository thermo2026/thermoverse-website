# ThermoVerse AWS IAM Role Overview and Handoff

Updated: September 16, 2026 (Taiwan Time)

This document isolates the IAM Role and permission-related parts of `aws/template.yaml` for AWS administrator review.

## Files to give your colleague

Send these four files together:

1. [`aws/template.yaml`](template.yaml) — the main AWS SAM / CloudFormation deployment template.
2. [`aws/lambda/handler.py`](lambda/handler.py) — the Lambda backend code referenced by the template.
3. [`aws/DEPLOYMENT_ACCESS_POLICY.json`](DEPLOYMENT_ACCESS_POLICY.json) — the deployment permissions policy for the `WebDev` Permission Set.
4. This document — the explanation of the IAM Roles and the deployment requirements.

The `website/` folder is the frontend and is deployed separately through Amplify Hosting. It is not required for the colleague to create the CRM backend stack.

`template.yaml` uses AWS SAM `CodeUri: lambda/`, so it should be deployed from the project folder with SAM or packaged first with the AWS CLI. It is not a self-contained Console upload until the Lambda code has been uploaded to S3. Do not send `crm/data/`, `website/config.js`, AWS access keys, SSO tokens, or any real inquiry records.

Recommended deployment command after the Permission Set is updated:

```sh
sam build --template-file aws/template.yaml
sam deploy --guided --stack-name thermoverse-crm-staging
```

Use `us-east-1` for the stack and enter the final Amplify HTTPS origin for `AllowedOrigin` when prompted.

## Executive summary

The CloudFormation template does not hard-code an `AWS::IAM::Role` resource. It uses AWS SAM `AWS::Serverless::Function` resources with `Policies`. During the SAM transform, CloudFormation creates one Lambda execution role for each function and attaches the requested DynamoDB permissions to that role.

The CRM backend uses three Lambda execution roles:

| Lambda function | Purpose | Required data permission |
|---|---|---|
| `SubmitInquiryFunction` | Receive and validate the public form, then write the inquiry | Read/write access to `InquiriesTable` |
| `ListInquiriesFunction` | Load inquiries for the CRM management page | Read access to `InquiriesTable` |
| `UpdateInquiryFunction` | Update inquiry status and internal notes | Read/write access to `InquiriesTable` |

All three roles are managed by CloudFormation. Do not manually rename or edit their trust policies in IAM. Future stack updates will keep the roles and their permissions synchronized.

## Role-related template excerpts

These are the relevant authorization sections extracted from `aws/template.yaml`:

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

`DynamoDBCrudPolicy` and `DynamoDBReadPolicy` are SAM policy templates. They scope Lambda access to the `InquiriesTable` created by this stack; the website code cannot use these roles to read arbitrary DynamoDB tables in the account.

## Permissions required by the deployment principal

These permissions belong to the person or Permission Set deploying the stack. They are separate from the Lambda execution roles. CloudFormation must be able to create the Lambda roles and attach their policies, so the deployment principal needs at least:

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

The deployment principal also needs permission to create and update the CloudFormation stack and its API Gateway, Lambda, DynamoDB, and Cognito resources. The full deployment policy is stored at:

`aws/DEPLOYMENT_ACCESS_POLICY.json`

`iam:PassRole` allows CloudFormation to pass the Lambda execution roles it creates to the Lambda service. It does not give Lambda the personal permissions of the person deploying the stack.

## Instructions for the AWS administrator

Please add the deployment policy to the `WebDev` Permission Set in IAM Identity Center, or create a temporary `ThermoVerseDeployment` Permission Set. Do not edit the `AWSReservedSSO_WebDev_...` role directly in IAM; that role is managed by IAM Identity Center.

If AWS managed policies are used for the initial staging deployment, confirm that the Permission Set includes:

- `AWSCloudFormationFullAccess`
- Permissions to create and update Lambda, DynamoDB, API Gateway, and Cognito resources
- `iam:CreateRole`, `iam:AttachRolePolicy`, `iam:PutRolePolicy`, and `iam:PassRole`
- `s3:GetObject`, `s3:PutObject`, and `s3:ListBucket` for the deployment artifact bucket

After staging is deployed and verified, remove any temporary administrator-level policy and use the narrower policy in `aws/DEPLOYMENT_ACCESS_POLICY.json`.

## Permissions that should not be given to Lambda execution roles

- Do not use `AdministratorAccess` as a Lambda execution-role permission.
- Do not allow the public form Lambda to read all DynamoDB tables.
- Do not give the public form Lambda Cognito administration permissions; Cognito protects the CRM management endpoints.
- Do not put AWS access keys, SSO tokens, or company email addresses in frontend files.

## Source and current status

- CloudFormation/SAM template: `aws/template.yaml`
- Lambda handlers: `aws/lambda/handler.py`
- Deployment permission policy: `aws/DEPLOYMENT_ACCESS_POLICY.json`
- The CloudFormation stack has not yet been created. This document describes the roles SAM will generate and the permissions required to deploy them; it does not mean those AWS resources already exist.
