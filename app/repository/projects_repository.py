from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.orm import sessionmaker


class ProjectsRepository:

    def __init__(self, engine: AsyncEngine, session_factory: sessionmaker):
        self.engine = engine
        self.session_factory = session_factory
