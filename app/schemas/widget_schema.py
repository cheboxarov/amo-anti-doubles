from pydantic import BaseModel, ConfigDict
from typing import Optional


class WidgetSchema(BaseModel):
    id: Optional[int]
    client_id: str
    secret_key: str

    class Config:
        orm_mode = True


class WidgetCreateSchema(BaseModel):
    client_id: str
    secret_key: str

    class Config:
        orm_mode = True


class WidgetUpdateSchema(BaseModel):
    client_id: Optional[str] = None
    secret_key: Optional[str] = None

    class Config:
        orm_mode = True
