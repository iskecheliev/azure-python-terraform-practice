# Azure practice course: Python SDK + Terraform

This repo is a hands-on course. The user is a beginner at writing code and works on two Macs, using this repo to move between them.

## How to tutor

- Small lessons. The user types and runs every command themselves, including setup like git. Claude only runs read-only checks to verify their work.
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
- Git mini-lesson: done. Repo is private at github.com/iskecheliev/azure-python-terraform-practice. Quiz answered.
- Lesson 2: Part A done. Applied 30 Oct 2026 **from the Air Mac** (state lives there): storage `sttfpractice6epyt1` + container `uploads`. Quiz answered; weak spots were what `init` does and what goes wrong if state is lost (name clash). GRS plan experiment set (plan only, then revert).
- 2 Nov 2026: user moved to the Mac mini. Not started yet: the GRS plan experiment and Part B step 1 (`lesson2_python/` doesn't exist yet).
  - Lesson 2 Terraform state (`terraform.tfstate`) is on the **Air** only. On the mini, check whether `lesson2_terraform/terraform.tfstate` exists. If not, do the Python steps only there (they need no state; the account name is `sttfpractice6epyt1`). Do not run `plan`/`apply` there: Terraform would try to recreate everything.
  - Mac mini setup: `git pull`, venv + `pip install -r requirements.txt`, `az login`, `az account set --subscription "Visual Studio Enterprise Subscription-Prod"`, `terraform init` in `lesson2_terraform/` (`.terraform/` is not in git).
- 2 Nov 2026: user chose to bring Lesson 7 remote state forward (after asking "why not commit state to git?"; we showed state holds the storage access keys). Plan, all done on the **Air** until the state is migrated:
  1. DONE: account is `stpracticetfstate48213`. User first gave themself Storage *Account* Contributor by mistake; fixed, and the management vs data role difference was taught. CLI: create RG `rg-tfstate-practice` + storage `stpracticetfstate<digits>` (blob versioning on) + container `tfstate` (via `container-rm`) + Storage Blob Data Contributor for the user on that account. NOT `rg-terraform-state`.
  2. DONE 2 Nov: state migrated to the `lesson2.tfstate` blob; `plan` says No changes. Add `backend "azurerm"` to `providers.tf` (key `lesson2.tfstate`, `use_azuread_auth = true`), then `terraform init -migrate-state`.
  3. Check: `plan` says No changes; the blob exists; then delete the local `terraform.tfstate*` files.
  4. On the Mac mini: `git pull`, `terraform init`, `plan` says No changes.
  Then resume Lesson 2 Part B. Lesson 7 later only needs modules (plus a quick review).
- Lesson 2 Part B: on hold until remote state is done. Step 1: copy the Lesson 1 script to point at the new account. The user's Storage Blob Data Contributor role is only on the old account `stpractice16407`, so the upload is expected to fail with a permissions error. Next: read that error, then add `azurerm_role_assignment` in Terraform, then delete `rg-prd-sdk-practice`.
- Always check the Terraform Registry for current provider versions; don't rely on memory (azurerm is 5.x as of Oct 2026).
- Second Mac: run `az account set --subscription "Visual Studio Enterprise Subscription-Prod"`. Its default subscription was a work one.
