from fastapi import FastAPI
from app.handlers import search_doubles_handler
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

app.include_router(search_doubles_handler.router)
app.add_middleware(AuthorizeMiddleware)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)
