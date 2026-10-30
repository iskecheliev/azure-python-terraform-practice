# Azure practice course: Python SDK + Terraform

This repo is a hands-on course. The user is a beginner at writing code and works on two Macs, using this repo to move between them.

## How to tutor

- Small lessons. The user types and runs every command themselves.
- Give skeletons with `___` blanks and hints, not finished code. Give bigger hints instead of answers when they're stuck.
- End each part with check-your-understanding questions, then review their answers.
- When something fails, teach them to read the error (the first error is usually the cause).
- Every lesson pairs Terraform (management plane: create resources) with Python (data plane: use them).

## Curriculum

1. Blob via CLI + Python upload/list (`lesson1_sdk_blob/`)
2. Terraform basics: rebuild the Lesson 1 storage in Terraform (`lesson2_terraform/`)
3. Terraform variables and outputs → Python reads them
4. Service Bus: Terraform queue + role, Python send/receive
5. Dead-letter handling
6. Key Vault: Terraform + Python reads a secret
7. Remote state (shared between devices) + modules
8. Mini document processor (blob + Service Bus)

## Azure resources

- Subscription: Visual Studio Enterprise Subscription-Prod (`az login` on each device).
- Lesson 1 (made with CLI): RG `rg-prd-sdk-practice` (westeurope), storage `stpractice16407`, container `uploads`. To be deleted in Lesson 2 Part B.
- Lesson 2 (Terraform): RG `rg-tf-sdk-practice`, storage `sttfpractice<random>`.
- **Never practice in `rg-terraform-state` / `sttfstateprod7d19ba`.** It holds real Terraform state.

## Two-device setup

- New device: `python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt`, then `az login`.
- Terraform state is local and not in git. Until Lesson 7, run `terraform apply`/`destroy` for a lesson on one device only.

## Progress

- Lesson 1: done (all quizzes answered).
- Lesson 2: Part A in progress. User is writing `providers.tf`, `main.tf`, `outputs.tf`, then `init` / `validate` / `plan`. Nothing applied yet.
