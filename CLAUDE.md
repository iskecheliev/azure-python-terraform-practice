# Azure practice course: Python SDK + Terraform

This repo is a hands-on course. The user is a beginner at writing code and works on two Macs, using this repo to move between them.

## How to tutor

- Small lessons. The user types and runs every command themselves, including setup like git. Claude only runs read-only checks to verify their work.
- Give skeletons with `___` blanks and hints, not finished code. Give bigger hints instead of answers when they're stuck.
- End each part with check-your-understanding questions, then review their answers.
- When something fails, teach them to read the error (the first error is usually the cause).
- Every lesson pairs Terraform (management plane: create resources) with Python (data plane: use them).

## Curriculum

Goal: practice for two exams with one hands-on project.
- **AI-200** (Azure AI Cloud Developer Associate, Python-based). It replaced AZ-204, which retired 31 Jul 2026. Covers containers, Cosmos DB/PostgreSQL/Redis with vectors, Service Bus + Event Grid, Functions, Key Vault + App Configuration, OpenTelemetry + KQL.
- **AZ-400** (DevOps Engineer Expert). Pipelines are 50–55% of it. The cert also needs AZ-104 or the developer associate cert (AI-200 is due to count; check the cert page).

Lesson types: numbered = Python SDK (data plane, AI-200) + Terraform (management plane); D = DevOps (AZ-400), automating the lessons before it. Code stays on GitHub; Azure Pipelines connects to it. Expensive resources (PostgreSQL, Redis, AKS, Container Apps) get `terraform destroy` at the end of each lesson.

1. Blob via CLI + Python upload/list (`lesson1_sdk_blob/`)
2. Terraform basics: rebuild the Lesson 1 storage in Terraform (`lesson2_terraform/`, `lesson2_python/`)
- D1. Azure DevOps project for the course + Azure Boards; link Boards to GitHub (`AB#` in commits).
- D2. Branching + pull requests: feature branches, GitHub branch protection on `main`; compare with an Azure Repos branch policy.
- D3. First YAML CI pipeline on the user's self-hosted agents: GitHub trigger, `terraform fmt -check` / `validate`, Python checks on every PR.
- D4. Service connection with workload identity federation (no secrets) + least-privilege roles; pipeline runs `terraform plan`.
- D5. Multi-stage: plan → environment with approval check → apply. Plan as a pipeline artifact.
3. Terraform variables and outputs → Python reads its config
4. Service Bus: queues, dead-letter queue, topics + subscriptions (Terraform + Python)
5. Azure Functions in Python: Service Bus trigger + blob output binding; Terraform creates it, the pipeline deploys it
- D6. Reusable pipelines: YAML templates, variables, variable groups.
6. Key Vault (secrets, rotation) + App Configuration; managed identity; Key Vault-linked variable group in the pipeline
7. Cosmos DB for NoSQL: SDK queries, RUs, indexing, consistency, change feed, vector search
- D7. Tests in the pipeline: pytest unit tests, publish results, code coverage, quality gate.
8. Containers: Dockerfile, ACR + ACR Tasks, App Service container, Container Apps with revisions + KEDA scaling on Service Bus
9. Event Grid: blob-created events → Function; filters, custom events, retries
10. Terraform modules (remote state already done)
- D8. Same CI in GitHub Actions with OIDC; security scanning (Dependabot, secret scanning, container + IaC scans).
11. PostgreSQL + pgvector (RAG pattern) and Azure Managed Redis (caching + vector index). Destroy the same day.
12. Observability: OpenTelemetry SDK → Application Insights, KQL queries, pipeline alerts (AI-200 + AZ-400)
13. AKS basics with manifest files, logs and events. Destroy the same day.
14. Capstone: mini document processor end to end, deployed by the pipeline. Then both practice assessments.

## Azure DevOps

- Org: https://dev.azure.com/iskecheliev. Existing projects: `My_First_Project`, `ai-document-processor` (the user's real project; don't touch it). Create a separate project for the course in D1.
- Agent pool `Self-Hosted-Linux`: two online agents on the user's local server, `hyper-v-dev-agent` and `hyper-v-prd-agent` (Ubuntu 26.04, agent 4.272.0, Python 3). Terraform isn't installed on them: install it in the pipeline (or on the agents, as a lesson).
- `az devops` CLI extension is installed on the Mac mini.

## Azure resources

- Subscription: Visual Studio Enterprise Subscription-Prod (`az login` on each device).
- Lesson 1 (made with CLI): RG `rg-prd-sdk-practice`. Deleted 2 Nov 2026.
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
  3. DONE (user confirmed 2 Nov): local state files deleted on the Air. Check: `plan` says No changes; the blob exists; then delete the local `terraform.tfstate*` files.
  4. On the Mac mini: `git pull`, `terraform init`, `plan` says No changes.
  Then resume Lesson 2 Part B. Lesson 7 later only needs modules (plus a quick review).
  - ALL DONE 2 Nov: Mac mini `plan` said No changes (state lock seen). Remote state works; `plan`/`apply` are now safe on either Mac (ignore older "Air only" notes above). Quiz: user knew `providers.tf` points to the state; wrongly thought losing the Blob Data role would fall back to keys (taught: `use_azuread_auth = true` means it fails with 403, and fails safely instead of recreating).
- Lesson 2 Part B (2 Nov, Mac mini): `lesson2_python/lesson2_blob.py` got 403 AuthorizationPermissionMismatch, user added `azurerm_role_assignment.me_blob` + `data.azurerm_client_config` (all blanks right), plan 1 to add, applied, script now uploads `hello_tf.txt`. Taught: DefaultAzureCredential never falls back to keys (repeat misconception, watch for it). Still open: the user's plan prediction, and the line number/status code from the first traceback. Old RG deleted, pushed. **Lesson 2 DONE.** User knew why `az` (not `terraform destroy`) deletes CLI-made resources.
- D1 (2-3 Nov, Mac mini): project `azure-practice-course` (Agile, private). Epic #2, Feature #3 "D1: Azure Boards", stories #4 (Closed), #5 (Active, linked to commit 56d6e62), #6 (Closed by commit cd28412 "Fixes AB#6"). Boards connected to the GitHub repo. CLI defaults set to org + project. Taught: `--type "User Story"`, capturing IDs in variables, case-sensitive `git add` on macOS, check `git status` before committing. Learned: in Agile, User Story "Resolved" is in the InProgress category, so `Fixes AB#` goes to Closed (Completed). Quiz weak spot: the *keyword* (`Fixes`) before `AB#` is what changes state, and only on the default branch. #3 and #5 closed, pushed (f54d4ea). **D1 DONE 3 Nov.** Epic #2 is still New (should be Active while the course runs). Next: D2.
- Always check the Terraform Registry for current provider versions; don't rely on memory (azurerm is 5.x as of Oct 2026).
- Second Mac: run `az account set --subscription "Visual Studio Enterprise Subscription-Prod"`. Its default subscription was a work one.
