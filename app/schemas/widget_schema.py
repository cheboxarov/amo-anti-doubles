from pydantic import BaseModel, ConfigDict
from typing import Optional


class WidgetSchema(BaseModel):

    id: Optional[int]
    client_id: str
    secret_key: str

    model_config = ConfigDict(from_attributes=True)
