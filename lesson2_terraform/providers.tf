terraform {
  backend "azurerm" {
    resource_group_name  = "rg-tfstate-practice"
    storage_account_name = "stpracticetfstate48213"
    container_name       = "tfstate"
    key                  = "lesson2.tfstate"

    use_azuread_auth = true
  }
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm" # hint: the company that makes Terraform
      version = "~> 5.0"
    }
    random = {
      source  = "hashicorp/random"
      version = "~> 3.9"
    }
  }
}

provider "azurerm" { # hint: same name as the key above
  features {}
}
