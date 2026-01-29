from typing import Any, Dict
from pydantic import BaseModel

class EnqueueReq(BaseModel):
    owner: str
    repository: str
    ref: str

class EnqueueResp(BaseModel):
    status: str
