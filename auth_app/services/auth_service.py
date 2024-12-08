from repository.widgets_repository import WidgetsRepository, WidgetNotFoundException
from repository.projects_repository import ProjectsRepository
from schemas.project_schema import ProjectSchema
from api.amo_tokens_api import AmoTokensApi
from loguru import logger


class AuthService:

    def __init__(
        self,
        widgets_repository: WidgetsRepository,
        projects_repository: ProjectsRepository,
    ):
        self.widgets_repository = widgets_repository
        self.projects_repository = projects_repository

    async def install_widget(
        self, code: str, client_id: str, subdomain: str
    ) -> ProjectSchema:
        widget = await self.widgets_repository.get_by_client_id(client_id)
        if not widget:
            raise WidgetNotFoundException(client_id=client_id)

        response = await AmoTokensApi.get_tokens_by_code(
            widget.client_id, widget.secret_key, code, subdomain
        )
        access_token, refresh_token = response.get("access_token"), response.get("refresh_token")

        project = await self.projects_repository.get_by_widget_and_subdomain(subdomain, widget.id)

        create_args = {
            "subdomain": subdomain,
            "access_token": access_token,
            "refresh_token": refresh_token,
            "widget_id": widget.id,
            "is_active": project.is_active if project else True,
            "is_admin": project.is_admin if project else False,
        }

        if project and not await self.projects_repository.delete(project.id):
            raise ValueError(f"Failed to delete project with id {project.id}")

        return await self.projects_repository.create(ProjectSchema(**create_args))

    async def update_token(self, project: ProjectSchema) -> ProjectSchema:
        widget_id = project.widget_id
        widget = await self.widgets_repository.get_by_id(widget_id)
        response = await AmoTokensApi.get_tokens_by_refresh(
            widget.client_id,
            widget.secret_key,
            project.refresh_token,
            project.subdomain,
        )
        project.access_token = response.get("access_token")
        project.refresh_token = response.get("refresh_token")
        await self.projects_repository.update(project.id, project)
        return project
