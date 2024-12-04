from fastapi import FastAPI
from handlers.search_doubles_handlers import router as s_d_router
from middlewares import AuthorizeMiddleware, ExcLoggingMiddleware
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import redis_client
from loguru_configurate import configurate_loguru
from services.telegram_logger_service import create_telegram_logger_from_dotenv
from config import REDIS_URL

loggers = [
    create_telegram_logger_from_dotenv()
]
configurate_loguru(loggers)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await redis_client.init_redis_pool(REDIS_URL)
    yield
    await redis_client.close_redis_client()


app = FastAPI(lifespan=lifespan)

app.include_router(s_d_router)
app.add_middleware(AuthorizeMiddleware)
app.add_middleware(ExcLoggingMiddleware)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
