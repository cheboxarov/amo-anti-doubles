from repository.repository import Repository
from .widgets_service import WidgetsService
from repository.repository import create_repositories
from .auth_service import AuthService
from .project_service import ProjectsService


class Service:

    def __init__(self, repository: Repository):
        self.repository = repository

    @property
    def widgets(self) -> WidgetsService:
        return WidgetsService(self.repository.widgets)

    @property
    def projects(self) -> ProjectsService:
        return ProjectsService(self.repository.projects)

    @property
    def auth(self) -> AuthService:
        return AuthService(self.repository.widgets, self.repository.projects)


async def create_services() -> Service:
    async with create_repositories() as repository:
        return Service(repository)
