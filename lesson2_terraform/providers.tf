terraform {
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
