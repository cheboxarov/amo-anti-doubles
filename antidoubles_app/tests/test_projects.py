import pytest
from httpx import AsyncClient
from main import app
from repository.models import BaseModel
from repository.repository import create_repositories
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite+aiosqlite:///:memory:"


@pytest.fixture(scope="function")
async def test_db():
    return create_repositories(DATABASE_URL)


@pytest.fixture
async def async_client(test_db):
    async def override_get_db():
        yield test_db

    app.dependency_overrides[create_repositories] = override_get_db

    async with AsyncClient(app=app, base_url="http://testserver") as client:
        yield client


@pytest.mark.asyncio
async def test_create_project(async_client):
    project_data = {
        "subdomain": "testproject",
        "is_active": True,
        "is_admin": False,
        "widget_id": 1,
    }
    response = await async_client.post("/projects", json=project_data)
    assert response.status_code == 201
    data = response.json()
    assert data["subdomain"] == project_data["subdomain"]
    assert data["is_active"] == project_data["is_active"]


@pytest.mark.asyncio
async def test_get_all_projects(async_client):
    response = await async_client.get("/projects")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


@pytest.mark.asyncio
async def test_get_project_by_id(async_client):
    response = await async_client.get("/projects/1")
    assert response.status_code == 200
    data = response.json()
    assert "id" in data


@pytest.mark.asyncio
async def test_patch_project(async_client):
    update_data = {"subdomain": "updatedproject", "is_admin": True}
    response = await async_client.patch("/projects/1", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["subdomain"] == update_data["subdomain"]
    assert data["is_admin"] == update_data["is_admin"]


@pytest.mark.asyncio
async def test_delete_project(async_client):
    response = await async_client.delete("/projects/1")
    assert response.status_code == 204
