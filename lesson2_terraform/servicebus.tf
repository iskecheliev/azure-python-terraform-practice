# 6. Service Bus namespace (the "account")
resource "azurerm_servicebus_namespace" "sb" {
  name                = "sb-tfpractice-${random_string.suffix.result}" # hint: reuse the storage account's random suffix resource
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  sku                 = "Standard" # hint: the tier that supports topics
  local_auth_enabled  = false      # hint: true = SAS keys allowed. We use Entra ID only, no keys.
  minimum_tls_version = "1.2"
}

# 7. Queue
resource "azurerm_servicebus_queue" "orders" {
  name         = "orders"
  namespace_id = azurerm_servicebus_namespace.sb.id

  max_delivery_count                   = 5    # after 5 failed tries → dead-letter queue (Part C)
  dead_lettering_on_message_expiration = true # expired messages → dead-letter queue too
}
