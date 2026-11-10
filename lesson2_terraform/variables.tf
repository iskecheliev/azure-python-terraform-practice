variable "location" {
  description = "Azure region for all resources"
  type        = string       # hint: text
  default     = "westeurope" # hint: the region in main.tf today
}

variable "blob_user_principal_id" {
  description = "Object ID of the person who gets Storage Blob Data Contributor"
  type        = string
  # no default on purpose: Terraform must be told
}
