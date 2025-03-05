from repository.projects_repository import ProjectsRepository
from repository.widgets_repository import WidgetsRepository, WidgetNotFoundException
from typing import Optional
from schemas.project_schema import ProjectSchema
from py_amo.services import AsyncAmoSession


class ProjectsService:

    def __init__(self, repository: ProjectsRepository, widgets_repo: WidgetsRepository):
        self.repository = repository
        self.widgets_repo = widgets_repo

    async def get_by_id(self, project_id: int) -> Optional[ProjectSchema]:
        return await self.repository.get_by_id(project_id)

    async def get_by_subdomain(self, subdomain: str) -> Optional[ProjectSchema]:
        return await self.repository.get_by_subdomain(subdomain)
    
    async def get_by_widget_and_subdomain(self, subdomain: str, widget_id: int) -> Optional[ProjectSchema]:
        if not await self.widgets_repo.get_by_id(widget_id):
            return WidgetNotFoundException(id=widget_id)
        return await self.repository.get_by_widget_and_subdomain(subdomain, widget_id)

    async def get_all(self) -> list[ProjectSchema]:
        return await self.repository.get_all()

    async def create(self, project: ProjectSchema) -> ProjectSchema:
        return await self.repository.create(project)

    async def update(self, project_id: int, project: ProjectSchema) -> ProjectSchema:
        return await self.repository.update(project_id, project)

    async def delete(self, project_id: int) -> bool:
        return await self.repository.delete(project_id)

    def get_api(self, project: ProjectSchema):
        """
        Get an instance of the AmoCRM API client for the given project.

        Args:
            project: The project to get the API client for.

        Returns:
            An instance of AsyncAmoSession.
        """
        return AsyncAmoSession(project.access_token, project.subdomain)
