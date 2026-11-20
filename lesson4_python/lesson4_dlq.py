import os
import sys

from azure.identity import DefaultAzureCredential
from azure.servicebus import ServiceBusClient, ServiceBusMessage, ServiceBusSubQueue

FQDN = os.environ.get("SERVICEBUS_FQDN")
QUEUE = "orders"

if not FQDN:
    print("SERVICEBUS_FQDN is not set.")
    sys.exit(1)

credential = DefaultAzureCredential()


with ServiceBusClient(fully_qualified_namespace=FQDN, credential=credential) as client:

    with client.get_queue_sender(queue_name=QUEUE) as sender:
        sender. send_messages(ServiceBusMessage("poison order"))
        print("Sent 1 poison message")

    with client.get_queue_receiver(queue_name=QUEUE) as receiver:
        attempt = 0
        while True:
            messages = receiver.receive_messages(max_message_count=1, max_wait_time=5)
            if not messages:
                print("Queue is empty, the message has left the main queue")
                break
            msg = messages[0]
            attempt += 1
            print(f"Attempt {attempt}: '{msg}', delivery_count={msg.delivery_count} ->giving up on it")
            receiver.abandon_message(msg)

    with client.get_queue_receiver(
        queue_name=QUEUE,
        sub_queue=ServiceBusSubQueue.DEAD_LETTER,
        max_wait_time=5
    ) as dlq_receiver:
        for msg in dlq_receiver:
            print(f"In DLQ: '{msg}'")
            print(f" reason: {msg.dead_letter_reason}")
            print(f"description: {msg.dead_letter_error_description}")
            print(f"delivery_count: {msg.delivery_count}")
            dlq_receiver.complete_message(msg)