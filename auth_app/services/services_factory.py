from repository.repositories_factory import RepositoriesFactory
from .widgets_service import WidgetsService
from repository.repositories_factory import create_repositories_factory
from .auth_service import AuthService
from .project_service import ProjectsService


class ServicesFactory:

    def __init__(self, repository: RepositoriesFactory):
        self.repository = repository

    @property
    def widgets(self) -> WidgetsService:
        return WidgetsService(self.repository.widgets)

    @property
    def projects(self) -> ProjectsService:
        return ProjectsService(self.repository.projects, self.repository.widgets)

    @property
    def auth(self) -> AuthService:
        return AuthService(self.repository.widgets, self.repository.projects)


async def create_services_factory() -> ServicesFactory:
    async with create_repositories_factory() as repository:
        return ServicesFactory(repository)
