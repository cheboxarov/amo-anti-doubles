from fastapi import FastAPI
from handlers.auth_handlers import router as auth_router
from handlers.search_doubles_handlers import router as s_d_router
from handlers.widgets_handlers import router as widgets_router
from handlers.projects_handlers import router as projects_router
from middlewares import AuthorizeMiddleware
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import redis_client


@asynccontextmanager
async def lifespan(app: FastAPI):
    await redis_client.init_redis_pool()
    yield
    await redis_client.close_redis_client()


app = FastAPI(lifespan=lifespan)

app.include_router(s_d_router)
app.include_router(auth_router)
app.include_router(widgets_router)
app.include_router(projects_router)
app.add_middleware(AuthorizeMiddleware)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
