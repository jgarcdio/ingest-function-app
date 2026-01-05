from azure.storage.queue import QueueClient, TextBase64EncodePolicy
from infra.settings import settings

_queue_client: QueueClient | None = None

def get_queue_client() -> QueueClient:
    global _queue_client
    if _queue_client is None:
        _queue_client = QueueClient.from_connection_string(
            settings.queue_conn,
            settings.queue_name,
            message_encode_policy=TextBase64EncodePolicy(),
        )
    return _queue_client
