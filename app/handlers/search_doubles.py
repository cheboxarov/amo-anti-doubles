from fastapi import APIRouter, Request, HTTPException
from doubles import GetDoublesRequest, DoubleEntityResponse
from py_amo.services import AsyncAmoSession
import redis_client
import json
from services.search_doubles import find_doubles

router = APIRouter()


async def check_searching_process(subdomain: str):
    search_processes = await redis_client.redis.get("search_processes")
    if search_processes is not None:
        search_processes = json.loads(search_processes)
    else:
        search_processes = []
    
    if subdomain in search_processes:
        raise HTTPException(status_code=400, detail="beasy")
    
    search_processes.append(subdomain)
    await redis_client.redis.set("search_processes", json.dumps(search_processes))


async def release_search_process(subdomain: str):
    search_processes = await redis_client.redis.get("search_processes")
    if search_processes is not None:
        search_processes = json.loads(search_processes)
        if subdomain in search_processes:
            search_processes.remove(subdomain)
            await redis_client.redis.set("search_processes", json.dumps(search_processes))


@router.post("/get_doubles/{subdomain}")
async def search_doubles(request_data: GetDoublesRequest, subdomain: str, request: Request):

    await check_searching_process(subdomain)
    try:
        session = AsyncAmoSession(request.state.token, subdomain)
        repos = {
            "contacts": session.contacts,
            "companies": session.companies
        }
        doubles = await find_doubles(repos[request_data.entity_type], session, ["Телефон", "Email"])
        return doubles
    finally:
        await release_search_process(subdomain)
