from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import declarative_base, relationship


BaseModel = declarative_base()


class ProjectModel(BaseModel):

    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    subdomain = Column(String, unique=True)
    access_token = Column(String, nullable=True)
    refresh_token = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    unactive_reason = Column(String, nullable=True)
    is_admin = Column(Boolean, default=False)
    widget_id = Column(
        Integer, ForeignKey("widgets.id", ondelete="CASCADE"), nullable=False
    )

    widget = relationship("WidgetModel", back_populates="projects")


class WidgetModel(BaseModel):

    __tablename__ = "widgets"

    id = Column(Integer, primary_key=True)
    client_id = Column(String)
    secret_key = Column(String)

    projects = relationship(
        "ProjectModel", back_populates="widget", cascade="all, delete"
    )
