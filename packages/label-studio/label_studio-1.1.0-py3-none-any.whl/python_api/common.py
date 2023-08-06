from pydantic import BaseModel
from .client import Client


class ClientObject(BaseModel):
    client: Client
