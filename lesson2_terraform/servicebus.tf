# 6. Service Bus namespace (the "account")
resource "azurerm_servicebus_namespace" "sb" {
  name                = "sb-tfpractice-${random_string.suffix.result}"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  sku                 = "Standard"
  local_auth_enabled  = false
  minimum_tls_version = "1.2"
}

# 7. Queue
resource "azurerm_servicebus_queue" "orders" {
  name         = "orders"
  namespace_id = azurerm_servicebus_namespace.sb.id

  max_delivery_count                   = 5    # after 5 failed tries → dead-letter queue (Part C)
  dead_lettering_on_message_expiration = true # expired messages → dead-letter queue too
}

# 8. Data roles for me: send + receive messages (not manage the namespace)
resource "azurerm_role_assignment" "me_sb_sender" {
  scope                = azurerm_servicebus_namespace.sb.id
  role_definition_name = "Azure Service Bus Data Sender"
  principal_id         = var.blob_user_principal_id
}

resource "azurerm_role_assignment" "me_sb_receiver" {
  scope                = azurerm_servicebus_namespace.sb.id
  role_definition_name = "Azure Service Bus Data Receiver"
  principal_id         = var.blob_user_principal_id
}
