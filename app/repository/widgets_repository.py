from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.orm import sessionmaker
from schemas.widget_schema import WidgetSchema
from typing import Optional, List
from sqlalchemy import select, insert, update, delete
from .models import WidgetModel


class WidgetsRepository:

    def __init__(self, engine: AsyncEngine, session_factory: sessionmaker):
        self.engine = engine
        self.session_factory = session_factory

    async def get_by_id(self, widget_id: int) -> Optional[WidgetSchema]:
        """Получить виджет по ид"""
        async with self.session_factory() as session:
            query = select(WidgetModel).where(WidgetModel.id == widget_id)
            result = await session.execute(query)
            widget = result.scalar_one_or_none()
            return WidgetSchema.model_validate(widget) if widget else None

    async def get_all(self) -> List[WidgetSchema]:
        """Получить все виджеты"""
        async with self.session_factory() as session:
            query = select(WidgetModel)
            result = session.execute(query)
            widgets = result.scalars().all()
            return [WidgetSchema.model_validate(widget) for widget in widgets]

    async def create(self, widget: WidgetSchema) -> WidgetSchema:
        """Создать виджет"""
        async with self.session_factory() as session:
            async with session.begin():
                query = (
                    insert(WidgetModel)
                    .values(client_id=widget.client_id, secret_key=widget.secret_key)
                    .returning(WidgetModel)
                )
                result = await session.execute(query)
                widget = result.fetchone()
                return WidgetSchema.model_validate(widget)

    async def update(
        self, widget_id: int, widget_data: WidgetSchema
    ) -> Optional[WidgetSchema]:
        """Обновить виджет"""
        async with self.session_factory() as session:
            async with session.begin():
                query = (
                    update(WidgetModel)
                    .where(WidgetModel.id == widget_id)
                    .values(
                        client_id=widget_data.client_id,
                        secret_key=widget_data.secret_key,
                    )
                    .returning(WidgetModel)
                )
                result = await session.execute(query)
                widget = result.fetchone()
                return WidgetSchema.model_validate(widget) if widget else None

    async def delete(self, widget_id: int) -> bool:
        """Удалить виджет по ид"""
        async with self.session_factory() as session:
            async with session.begin():
                query = delete(WidgetModel).where(WidgetModel.id == widget_id)
                result = session.execute(query)
                return result.rowcount > 0
