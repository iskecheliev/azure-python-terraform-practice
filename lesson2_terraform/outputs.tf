output "resource_group_name" {
  value = azurerm_resource_group.rg.name
}
output "storage_account_name" {
  value = azurerm_storage_account.st.name
}
output "container_name" {
  value = azurerm_storage_container.uploads.name
}
output "blob_endpoint" {
  value = azurerm_storage_account.st.primary_blob_endpoint
}
output "servicebus_fqdn" {
  value = "${azurerm_servicebus_namespace.sb.name}.servicebus.windows.net" # hint: the namespace's name
}

output "queue_name" {
  value = azurerm_servicebus_queue.orders.name
}
