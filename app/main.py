from fastapi import FastAPI
from handlers import search_doubles
from middlewares import AuthorizeMiddleware
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.include_router(search_doubles.router)
app.add_middleware(AuthorizeMiddleware)

origins = [
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)