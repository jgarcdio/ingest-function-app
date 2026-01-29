import os
from pydantic import BaseModel, Field, ValidationError

class Settings(BaseModel):
    queue_conn: str = Field(alias="QUEUE_CONN")
    queue_name: str = Field(alias="QUEUE_NAME")

    github_token: str = Field(alias="GITHUB_TOKEN")

    @classmethod
    def load(cls) -> "Settings":
        try:
            return cls.model_validate({
                "QUEUE_CONN": os.getenv("QUEUE_CONN"),
                "QUEUE_NAME": os.getenv("QUEUE_NAME"),

                "GITHUB_TOKEN": os.getenv("GITHUB_TOKEN"),
            })     
        except ValidationError as exc:
            raise RuntimeError("Configuración inválida o incompleta") from exc

settings = Settings.load()