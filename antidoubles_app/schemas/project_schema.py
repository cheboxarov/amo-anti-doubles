from pydantic import BaseModel
from typing import Optional


class ProjectBaseSchema(BaseModel):
    subdomain: str
    is_active: bool = True
    is_admin: bool = False
    widget_id: int
    unactive_reason: Optional[str] = None


class ProjectCreateSchema(ProjectBaseSchema):
    pass


class ProjectUpdateSchema(BaseModel):
    subdomain: Optional[str] = None
    is_active: Optional[bool] = None
    is_admin: Optional[bool] = None
    widget_id: Optional[int] = None
    access_token: Optional[str] = None
    refresh_token: Optional[str] = None
    unactive_reason: Optional[str] = None


class ProjectSchema(ProjectBaseSchema):
    id: int
    access_token: Optional[str] = None
    refresh_token: Optional[str] = None

    class Config:
        orm_mode = True
