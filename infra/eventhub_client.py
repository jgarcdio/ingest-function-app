import json
from typing import Optional

from azure.eventhub import EventHubProducerClient, EventData
from infra.settings import settings

_producer: Optional[EventHubProducerClient] = None

def get_eventhub_producer() -> EventHubProducerClient:
    global _producer
    if _producer is None:
        if settings.eventhub_name:
            _producer = EventHubProducerClient.from_connection_string(
                conn_str=settings.eventhub_conn,
                eventhub_name=settings.eventhub_name,
            )
        else:
            _producer = EventHubProducerClient.from_connection_string(
                conn_str=settings.eventhub_conn,
            )
    return _producer

def send_event(payload: dict, partition_key: str | None = None) -> None:
    producer = get_eventhub_producer()
    event = EventData(json.dumps(payload))

    with producer:
        batch = producer.create_batch(partition_key=partition_key)
        batch.add(event)
        producer.send_batch(batch)
