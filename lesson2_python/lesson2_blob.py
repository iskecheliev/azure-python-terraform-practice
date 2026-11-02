# --- 1. Imports: bring in the tools we need ---
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient

# --- 2. Settings ---
ACCOUNT_URL = "https://sttfpractice6epyt1.blob.core.windows.net/"   # blank A
CONTAINER = "uploads"                                    # blank B
FILE_TO_UPLOAD = "hello_tf.txt"

# --- 3. Credential: who am I? ---
credential = DefaultAzureCredential()                            # blank C

# --- 4. Client: what am I talking to? ---
service_client = BlobServiceClient(ACCOUNT_URL, credential)
container_client = service_client.get_container_client(CONTAINER)

# --- 5. Operation 1: upload ---
with open(FILE_TO_UPLOAD, "rb") as f:
    container_client.upload_blob(name=FILE_TO_UPLOAD, data=f, overwrite=True)   # blank D
print(f"Uploaded {FILE_TO_UPLOAD}")

# --- 6. Operation 2: list everything in the container ---
print("Container contents:")
for blob in container_client.list_blobs():                  # blank E
    print(f"  - {blob.name}  ({blob.size} bytes)")