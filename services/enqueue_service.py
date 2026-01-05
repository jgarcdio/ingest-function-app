import json
from typing import Any, Dict, Set
from infra.settings import settings
from infra.blob_client import get_raw_container_client
from infra.queue_client import get_queue_client
from logger.logging import configure_logging
from utils.constants import REQUIRED_SUBFOLDERS

logger = configure_logging()

def validate_required_subfolders(app_name: str) -> None:
    raw_container = get_raw_container_client()
    raw_prefix = f"{app_name}/"
    found: Set[str] = set()

    logger.info(f"Validando subcarpetas requeridas para app={app_name}")

    for blob in raw_container.list_blobs(name_starts_with=raw_prefix):
        rel_path = blob.name[len(raw_prefix):]
        for subfolder in list(REQUIRED_SUBFOLDERS - found):
            if rel_path.startswith(subfolder):
                found.add(subfolder)

        if found == REQUIRED_SUBFOLDERS:
            break

    if found != REQUIRED_SUBFOLDERS:
        missing = sorted(list(REQUIRED_SUBFOLDERS - found))
        logger.warning(f"Faltan subcarpetas para app={app_name}: {missing}")
        raise ValueError(f"Faltan subcarpetas requeridas: {missing}")
    
def build_payload(app_name: str) -> Dict[str, Any]:
    return {
        "app": app_name,
        "rawPath": f"{settings.raw_container}/{app_name}/",
        "outDocsPath": f"{settings.docs_container}/{app_name}/docs/",
    }

def enqueue_message(payload: dict) -> None:
    queue_client = get_queue_client()
    queue_client.send_message(json.dumps(payload))

def enqueue_app(app_name: str) -> Dict[str, Any]:
    validate_required_subfolders(app_name)
    payload = build_payload(app_name)
    enqueue_message(payload)
    return payload