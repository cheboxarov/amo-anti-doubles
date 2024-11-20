from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import declarative_base


BaseModel = declarative_base()


class Project(BaseModel):

    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    subdomain = Column(String, unique=True)
    access_token = Column(String, nullable=True)
    refresh_token = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)


class WidgetModel(BaseModel):

    __tablename__ = "widgets"

    id = Column(Integer, primary_key=True)
    client_id = Column(String)
    secret_key = Column(String)
