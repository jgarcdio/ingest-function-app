from typing import Any, Dict
from pydantic import BaseModel


class EnqueueReq(BaseModel):
    app: str


class EnqueueResp(BaseModel):
    status: str
    payload: Dict[str, Any]