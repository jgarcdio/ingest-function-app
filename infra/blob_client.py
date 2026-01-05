from azure.storage.blob import BlobServiceClient, ContainerClient
from infra.settings import settings

_blob_service_client: BlobServiceClient | None = None

def get_blob_service_client() -> BlobServiceClient:
    global _blob_service_client
    if _blob_service_client is None:
        _blob_service_client = BlobServiceClient.from_connection_string(settings.blob_conn)
    return _blob_service_client

def get_raw_container_client() -> ContainerClient:
    return get_blob_service_client().get_container_client(settings.raw_container)
