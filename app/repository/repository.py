from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, AsyncEngine
from sqlalchemy.orm import sessionmaker
from config import DATABASE_URL
from .models import BaseModel
from .projects_repository import ProjectsRepository
from .widgets_repository import WidgetsRepository


class Repository:

    def __init__(self, engine: AsyncEngine, async_session_factory: sessionmaker):
        self.engine = engine
        self.async_session_factory = async_session_factory

    async def init_db(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(BaseModel.metadata.create_all)

    async def close(self):
        await self.engine.dispose()

    @property
    def projects(self) -> ProjectsRepository:
        return ProjectsRepository(self.engine, self.async_session_factory)

    @property
    def widgets(self) -> WidgetsRepository:
        return WidgetsRepository(self.engine, self.async_session_factory)


def create_repositories() -> Repository:
    engine = create_async_engine(DATABASE_URL)
    async_session_factory = sessionmaker(
        engine, expire_on_commit=False, class_=AsyncSession
    )
    return Repository(engine, async_session_factory)
