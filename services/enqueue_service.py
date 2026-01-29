import json
from infra.github_client import validate_project_structure
from infra.queue_client import get_queue_client
from logger.logging import configure_logging
from utils.constants import REQUIRED_SUBFOLDERS

logger = configure_logging()

def enqueue_message(payload: dict) -> None:
    queue_client = get_queue_client()
    queue_client.send_message(json.dumps(payload))

def enqueue_app(owner: str, repository: str, ref: str) -> None:
    validate_project_structure(owner, repository, ref)

    data_to_send = {
        "owner": owner,
        "repository": repository,
        "ref": ref,
    }

    logger.info(f"data_to_send={data_to_send}")
    enqueue_message({
        "owner": owner,
        "repository": repository,
        "ref": ref,
    })
