# 1. Resource group
resource "azurerm_resource_group" "rg" {
  name     = "rg-tf-sdk-practice" # hint: CLAUDE.md, Lesson 2 RG name
  location = "westeurope"         # hint: same region as Lesson 1
}

# 2. Random suffix for a unique storage name
resource "random_string" "suffix" {
  length  = 6
  upper   = false # hint: storage names allow no capital letters
  special = false # hint: no symbols allowed either
}

# 3. Storage account
resource "azurerm_storage_account" "st" {
  name                     = "sttfpractice${random_string.suffix.result}"
  resource_group_name      = azurerm_resource_group.rg.name
  location                 = azurerm_resource_group.rg.location
  account_tier             = "Standard"
  account_replication_type = "LRS" # hint: cheapest option, 3 letters
}

# 4. Container
resource "azurerm_storage_container" "uploads" {
  name                  = "uploads"
  storage_account_id    = azurerm_storage_account.st.id
  container_access_type = "private"
}
