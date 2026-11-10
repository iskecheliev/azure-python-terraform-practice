import os
import sys
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient

# --- Settings come from the environment, not from the code ---
ACCOUNT_URL = os.environ.get("STORAGE_BLOB_ENDPOINT")          # hint: name it STORAGE_BLOB_ENDPOINT
CONTAINER = "uploads"

if not ACCOUNT_URL:
    print("STORAGE_BLOB_ENDPOINT is not set. Run:")
    print('  export STORAGE_BLOB_ENDPOINT=$(terraform -chdir=lesson2_terraform output -raw blob_endpoint)')
    sys.exit(1)                            # hint: 0 means success; anything else means failure

credential = DefaultAzureCredential()
service_client = BlobServiceClient(account_url=ACCOUNT_URL, credential=credential)
container_client = service_client.get_container_client(CONTAINER)

print(f"Account: {ACCOUNT_URL}")
for blob in container_client.list_blobs():
    print(f"  - {blob.name}  ({blob.size} bytes)")