from fastapi import APIRouter, Request, HTTPException
from schemas.doubles_schemas import GetDoublesRequest, DoubleEntityResponse
from py_amo.services import AsyncAmoSession
import redis_client
import json
from services.search_doubles_service import FindDoublesService
from contextlib import asynccontextmanager
from typing import TypedDict
from schemas.project_schema import ProjectSchema

router = APIRouter()


@asynccontextmanager
async def search_process_manager(subdomain: str):
    """
    Context manager to manage search processes in Redis

    :param subdomain: subdomain of amoCRM
    :raises HTTPException: if search process is already running
    :return:
    """

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


@router.post("/get_doubles")
async def search_doubles(request_data: GetDoublesRequest, request: Request):
    """
    Search for doubles in amoCRM by phone or email

    :param request_data: GetDoublesRequest with entity_type and search_type
    :param subdomain: subdomain of amoCRM
    :param request: FastAPI request to get token from state
    :return: dict with doubles
    :raises HTTPException: if search process is already running
    """
    project: ProjectSchema = request.state.project
    async with search_process_manager(project.subdomain):
        session = AsyncAmoSession(project.access_token, project.subdomain)
        repos = {"contacts": session.contacts, "companies": session.companies}
        service = FindDoublesService(repos[request_data.entity_type], session)
        doubles = await service.find_doubles(["Телефон", "Email"])
        return {"doubles": doubles}
