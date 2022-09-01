from pydantic import BaseModel
from typing import Literal
import datetime



class Client(BaseModel):
    """Client request model"""
    cid: str
    public_key: str


class ClientData(BaseModel):
    """Client data model"""
    cid: str
    data: str
    signature: str


personSchema = {
    "type": "object",
    "properties": {
        "person_id": {"type": "string"},
        "name": {"type": "string"},
    },
}