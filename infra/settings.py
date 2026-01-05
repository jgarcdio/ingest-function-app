import os
from pydantic import BaseModel, Field, ValidationError

class Settings(BaseModel):
    blob_conn: str = Field(alias="BLOB_CONN")
    queue_conn: str = Field(alias="QUEUE_CONN")
    queue_name: str = Field(alias="QUEUE_NAME")

    raw_container: str = Field(alias="RAW_CONTAINER")
    docs_container: str = Field(alias="DOCS_CONTAINER")

    @classmethod
    def load(cls) -> "Settings":
        try:
            return cls.model_validate({
                "BLOB_CONN": os.getenv("BLOB_CONN"),
                "QUEUE_CONN": os.getenv("QUEUE_CONN"),
                "QUEUE_NAME": os.getenv("QUEUE_NAME"),
                "RAW_CONTAINER": os.getenv("RAW_CONTAINER"),
                "DOCS_CONTAINER": os.getenv("DOCS_CONTAINER"),
            })     
        except ValidationError as exc:
            raise RuntimeError("Configuración inválida o incompleta") from exc

settings = Settings.load()