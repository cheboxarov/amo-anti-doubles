from fastapi import APIRouter, Request, HTTPException
from app.schemas.doubles_schemas import GetDoublesRequest, DoubleEntityResponse
from py_amo.services import AsyncAmoSession
import redis_client
import json
from app.services.search_doubles_service import FindDoublesService
from contextlib import asynccontextmanager

router = APIRouter()


@asynccontextmanager
async def search_process_manager(subdomain: str):
    search_processes = await redis_client.redis.get("search_processes")
    if search_processes is not None:
        search_processes = json.loads(search_processes)
    else:
        search_processes = []

    if subdomain in search_processes:
        raise HTTPException(status_code=400, detail="beasy")

    search_processes.append(subdomain)
    await redis_client.redis.set("search_processes", json.dumps(search_processes))

    try:
        yield
    finally:
        if subdomain in search_processes:
            search_processes.remove(subdomain)
        await redis_client.redis.set("search_processes", json.dumps(search_processes))


@router.post("/get_doubles/{subdomain}")
async def search_doubles(
    request_data: GetDoublesRequest, subdomain: str, request: Request
):

    async with search_process_manager(subdomain):
        session = AsyncAmoSession(request.state.token, subdomain)
        repos = {"contacts": session.contacts, "companies": session.companies}
        service = FindDoublesService(repos[request_data.entity_type], session)
        doubles = await service.find_doubles(["Телефон", "Email"])
        return {"doubles": doubles}
