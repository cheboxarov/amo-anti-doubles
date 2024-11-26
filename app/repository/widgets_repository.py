from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession
from sqlalchemy.orm import sessionmaker
from schemas.widget_schema import WidgetSchema
from typing import Optional, List
from sqlalchemy import select, insert, update, delete
from .models import WidgetModel
from sqlalchemy.sql import expression


class WidgetsRepository:
    def __init__(
        self, engine: AsyncEngine, session_factory: sessionmaker[AsyncSession]
    ):
        self.engine = engine
        self.session_factory = session_factory

    async def get_by_filter(
        self, filter: expression.BinaryExpression
    ) -> Optional[WidgetSchema]:
        """Получить виджет по фильтру"""
        async with self.session_factory() as session:
            query = select(WidgetModel).where(filter)
            result = await session.execute(query)
            widget = result.scalar_one_or_none()
            if widget:
                return WidgetSchema.model_validate(widget.__dict__)
            return None

    async def get_by_id(self, widget_id: int) -> Optional[WidgetSchema]:
        """Получить виджет по id"""
        return await self.get_by_filter(WidgetModel.id == widget_id)

    async def get_by_client_id(self, client_id: str):
        """Получить виджет по клиент ид"""
        return await self.get_by_filter(WidgetModel.client_id == client_id)

    async def get_all(self) -> List[WidgetSchema]:
        """Получить все виджеты"""
        async with self.session_factory() as session:
            query = select(WidgetModel)
            result = await session.execute(query)
            widgets = result.scalars().all()
            return [WidgetSchema.model_validate(widget.__dict__) for widget in widgets]

    async def create(self, widget: WidgetSchema) -> Optional[WidgetSchema]:
        """Создать виджет"""
        async with self.session_factory() as session:
            async with session.begin():
                query = (
                    insert(WidgetModel)
                    .values(client_id=widget.client_id, secret_key=widget.secret_key)
                    .returning(WidgetModel)
                )
                result = await session.execute(query)
                widget_row = result.fetchone()
                if widget_row:
                    return WidgetSchema.model_validate(
                        widget_row.WidgetModel, from_attributes=True
                    )
            return None

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
                widget_row = result.fetchone()
                if widget_row:
                    return WidgetSchema.model_validate(
                        widget_row.WidgetModel, from_attributes=True
                    )
            return None

    async def delete(self, widget_id: int) -> bool:
        """Удалить виджет по id"""
        async with self.session_factory() as session:
            async with session.begin():
                query = delete(WidgetModel).where(WidgetModel.id == widget_id)
                result = await session.execute(query)
                return result.rowcount > 0
