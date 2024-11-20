from repository.repository import Repository
from .widgets_service import WidgetsService
from repository.repository import create_repositories


class Service:

    def __init__(self, repository: Repository):
        self.repository = repository

    @property
    def widgets(self) -> WidgetsService:
        return WidgetsService(self.repository.widgets)


def create_services() -> Service:
    return Service(create_repositories())
