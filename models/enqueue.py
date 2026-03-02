from typing import Any, Dict
from pydantic import BaseModel


class EnqueueReq(BaseModel):
    applicationName: str


class EnqueueResp(BaseModel):
    runId: str