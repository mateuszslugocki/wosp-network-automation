from pydantic import BaseModel


class DeviceConfig(BaseModel):
    name: str
    config: str
