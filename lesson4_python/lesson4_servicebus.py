import os
import sys

from azure.identity import DefaultAzureCredential
from azure.servicebus import ServiceBusClient, ServiceBusMessage

FQDN = os.environ.get("SERVICEBUS_FQDN")     
QUEUE = "orders"

if not FQDN:
    print("SERVICEBUS_FQDN is not set. Run:")
    print("  export SERVICEBUS_FQDN=$(terraform -chdir=lesson2_terraform output -raw servicebus_fqdn)")
    sys.exit(1)                 

credential = DefaultAzureCredential()

with ServiceBusClient(fully_qualified_namespace=FQDN, credential=credential) as client:
    # Send 3 messages
    with client.get_queue_sender(queue_name=QUEUE) as sender:
        for i in range(1, 4):
            sender.send_messages(ServiceBusMessage(f"order {i}"))
        print("Sent 3 messages")

    # Receive them
    with client.get_queue_receiver(queue_name=QUEUE, max_wait_time=5) as receiver:
        for msg in receiver:
            print(f"Received: {msg}")
            receiver.complete_message(msg)      