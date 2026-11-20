import json
import os
import sys

from azure.identity import DefaultAzureCredential
from azure.servicebus import ServiceBusClient, ServiceBusMessage, ServiceBusSubQueue

FQDN = os.environ.get("SERVICEBUS_FQDN")
QUEUE = "orders"

if not FQDN:
    print("SERVICEBUS_FQDN is not set.")
    sys.exit(1)

orders = [
    {"order_id": 1, "qty": 2},   # good order
    {"order_id": 2},             # broken: no "qty"
]

credential = DefaultAzureCredential()

with ServiceBusClient(fully_qualified_namespace=FQDN, credential=credential) as client:

    # 1. Send both orders as JSON text
    with client.get_queue_sender(queue_name=QUEUE) as sender:
        for order in orders:
            sender.send_messages(ServiceBusMessage(json.___(order)))   # hint: dict -> text. "dump to string"
        print(f"Sent {len(orders)} orders")

    # 2. A real receiver: check each order, then decide
    with client.get_queue_receiver(queue_name=QUEUE, max_wait_time=5) as receiver:
        for msg in receiver:
            order = json.___(str(msg))           # hint: text -> dict. "load from string"
            if "qty" in order:
                print(f"OK:  order {order['order_id']} processed")
                receiver.___(msg)                # hint: success, delete it
            else:
                print(f"BAD: order {order['order_id']} has no qty -> dead-lettering")
                receiver.___(                    # hint: the call that parks it in the DLQ now
                    msg,
                    reason="___",                # hint: your own short label, e.g. MissingField
                    error_description="Order has no 'qty' field",
                )

    # 3. Look in the DLQ
    with client.get_queue_receiver(
        queue_name=QUEUE,
        sub_queue=ServiceBusSubQueue.DEAD_LETTER,
        max_wait_time=5,
    ) as dlq_receiver:
        for msg in dlq_receiver:
            print(f"In DLQ: {msg}")
            print(f"  reason:         {msg.dead_letter_reason}")
            print(f"  description:    {msg.dead_letter_error_description}")
            print(f"  delivery_count: {msg.delivery_count}")
            dlq_receiver.complete_message(msg)