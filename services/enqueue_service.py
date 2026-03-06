import uuid
from typing import Any, Dict, Set

from infra.settings import settings
from infra.blob_client import get_raw_container_client
from infra.eventhub_client import send_event
from logger.logging import configure_logging
from utils.constants import DOCS_FOLDER, REQUIRED_SUBFOLDERS

logger = configure_logging()

def validate_required_subfolders(applicationName: str) -> None:
    raw_container = get_raw_container_client()
    raw_prefix = f"{applicationName}/"
    found: Set[str] = set()

    logger.info("Validando subcarpetas requeridas para app=%s", applicationName)
    for blob in raw_container.list_blobs(name_starts_with=raw_prefix):
        rel_path = blob.name[len(raw_prefix):]
        for subfolder in list(REQUIRED_SUBFOLDERS - found):
            if rel_path.startswith(subfolder):
                found.add(subfolder)

        if found == REQUIRED_SUBFOLDERS:
            break

    if found != REQUIRED_SUBFOLDERS:
        missing = sorted(list(REQUIRED_SUBFOLDERS - found))
        logger.warning("Faltan subcarpetas para app=%s: %s", applicationName, missing)
        raise ValueError(f"Faltan subcarpetas requeridas: {missing}")

def build_payload(applicationName: str) -> Dict[str, Any]:
    return {
        "runId": generate_run_id(),
        "applicationName": applicationName,
        "rawPath": f"{settings.raw_container}/{applicationName}/",
        "outDocsPath": f"{settings.docs_container}/{applicationName}/{DOCS_FOLDER}/",
    }

def enqueue_message(payload: dict) -> None:
    send_event(payload, partition_key=payload.get("applicationName"))

def enqueue_app(applicationName: str) -> Dict[str, Any]:
    validate_required_subfolders(applicationName)
    payload = build_payload(applicationName)
    enqueue_message(payload)
    return payload

def generate_run_id() -> str:
    return str(uuid.uuid4().hex[:10])