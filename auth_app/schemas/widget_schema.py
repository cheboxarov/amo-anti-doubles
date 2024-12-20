from pydantic import BaseModel, ConfigDict
from typing import Optional


class WidgetSchema(BaseModel):
    id: Optional[int]
    name: str
    client_id: str
    secret_key: str

    class Config:
        from_attributes = True


class WidgetCreateSchema(BaseModel):
    name: str
    client_id: str
    secret_key: str

    class Config:
        from_attributes = True


class WidgetUpdateSchema(BaseModel):
    name: Optional[str] = None
    client_id: Optional[str] = None
    secret_key: Optional[str] = None

    class Config:
        from_attributes = True
