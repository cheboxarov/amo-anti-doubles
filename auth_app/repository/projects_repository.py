from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession
from sqlalchemy.orm import sessionmaker, joinedload
from schemas.project_schema import ProjectSchema
from typing import Optional, List
from sqlalchemy import select, update, delete, insert
from .models import ProjectModel
from sqlalchemy.sql import expression


class ProjectsRepository:

    def __init__(
        self, engine: AsyncEngine, session_factory: sessionmaker[AsyncSession]
    ):
        self.engine = engine
        self.session_factory = session_factory

    async def get_by_filter(
        self, filter: expression.BinaryExpression
    ) -> Optional[ProjectSchema]:
        async with self.session_factory() as session:
            query = (
                select(ProjectModel)
                .where(filter)
                .options(joinedload(ProjectModel.widget))
            )
            result = await session.execute(query)
            project = result.scalar_one_or_none()
            return ProjectSchema.model_validate(project.__dict__) if project else None

    async def get_by_id(self, project_id: int) -> Optional[ProjectSchema]:
        return await self.get_by_filter(ProjectModel.id == project_id)

    async def get_by_subdomain(self, subdomain: str) -> Optional[ProjectSchema]:
        return await self.get_by_filter(ProjectModel.subdomain == subdomain)
    
    async def get_by_widget_and_subdomain(self, subdomain: str, widget_id: int) -> Optional[ProjectSchema]:
        return await self.get_by_filter(ProjectModel.subdomain == subdomain and ProjectModel.widget_id == widget_id)

    async def get_all(self) -> List[ProjectSchema]:
        async with self.session_factory() as session:
            query = select(ProjectModel).options(joinedload(ProjectModel.widget))
            result = await session.execute(query)
            projects = result.scalars().all()
            return [
                ProjectSchema.model_validate(project.__dict__) for project in projects
            ]

    async def create(self, project: ProjectSchema) -> Optional[ProjectSchema]:
        async with self.session_factory() as session:
            async with session.begin():
                query = (
                    insert(ProjectModel)
                    .values(**project.model_dump(exclude_unset=True))
                    .returning(ProjectModel)
                )
                result = await session.execute(query)
                created_project = result.fetchone()
                if created_project:
                    return ProjectSchema.model_validate(
                        created_project.ProjectModel, from_attributes=True
                    )
            return None

    async def update(
        self, project_id: int, project: ProjectSchema
    ) -> Optional[ProjectSchema]:
        async with self.session_factory() as session:
            async with session.begin():
                query = (
                    update(ProjectModel)
                    .where(ProjectModel.id == project_id)
                    .values(**project.model_dump(exclude_unset=True))
                    .returning(ProjectModel)
                )
                result = await session.execute(query)
                updated_project = result.fetchone()
                if updated_project:
                    return ProjectSchema.model_validate(
                        updated_project.ProjectModel, from_attributes=True
                    )
            return None

    async def delete(self, project_id: int) -> bool:
        async with self.session_factory() as session:
            async with session.begin():
                query = delete(ProjectModel).where(ProjectModel.id == project_id)
                result = await session.execute(query)
                return result.rowcount > 0
