import os
from pydantic import BaseModel, Field, ValidationError

class Settings(BaseModel):
    blob_conn: str = Field(alias="BLOB_CONN")

    eventhub_conn: str = Field(alias="EVENTHUB_CONN")
    eventhub_name: str | None = Field(default=None, alias="EVENTHUB_NAME")

    raw_container: str = Field(alias="RAW_CONTAINER")
    docs_container: str = Field(alias="DOCS_CONTAINER")

    @classmethod
    def load(cls) -> "Settings":
        try:
            return cls.model_validate({
                "BLOB_CONN": os.getenv("BLOB_CONN"),
                "EVENTHUB_CONN": os.getenv("EVENTHUB_CONN"),
                "EVENTHUB_NAME": os.getenv("EVENTHUB_NAME"),
                "RAW_CONTAINER": os.getenv("RAW_CONTAINER"),
                "DOCS_CONTAINER": os.getenv("DOCS_CONTAINER"),
            })
        except ValidationError as exc:
            raise RuntimeError("Configuración inválida o incompleta") from exc

settings = Settings.load()