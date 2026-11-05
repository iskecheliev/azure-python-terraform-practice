# # Azure Practice: Python, Terraform & DevOps

## Goal

Preparing for two Microsoft exams:
- **AI-200**: Azure AI Cloud Developer Associate
- **AZ-400**: DevOps Engineer Expert

## Contents

- `lesson1_sdk_blob/`: Create Storage account(SA)  with Azure CLI and upload blob in a container using python.
- `lesson2_terraform/`: Create SA and contaner using Terraform 
- `lesson2_python/`: Use Python to upload file in SA created with Terraform

## Setup on a new Mac

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
az login
az account set --subscription "Visual Studio Enterprise Subscription-Prod" ## or DEV
```

## New Line to test Protect-main -second try

## CI

Every pull request to `main` runs the `ci` pipeline in Azure Pipelines (self-hosted agent). It checks:
- Terraform format check
- Terraform validate
- Python syntax check