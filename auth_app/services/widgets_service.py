from repository.widgets_repository import WidgetsRepository
from typing import Optional
from schemas.widget_schema import WidgetSchema


class WidgetsService:

    def __init__(self, repository: WidgetsRepository):
        self.repository = repository

    async def get_by_id(self, widget_id: int) -> Optional[WidgetSchema]:
        return await self.repository.get_by_id(widget_id)
    
    async def get_by_name(self, widget_name: str) -> Optional[WidgetSchema]:
        return await self.repository.get_by_name(widget_name)

    async def get_all(self) -> list[WidgetSchema]:
        return await self.repository.get_all()

    async def create(self, widget: WidgetSchema) -> WidgetSchema:
        return await self.repository.create(widget)

    async def update(self, widget_id: int, widget_data: WidgetSchema) -> WidgetSchema:
        return await self.repository.update(widget_id, widget_data)

    async def delete(self, widget_id: int) -> bool:
        return await self.repository.delete(widget_id)
