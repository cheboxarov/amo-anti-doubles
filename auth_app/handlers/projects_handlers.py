from schemas.project_schema import (
    ProjectSchema,
    ProjectUpdateSchema,
    ProjectCreateSchema,
    GetMeRequest,
    ProjectWithoutRefreshSchema
)
from fastapi import APIRouter, Depends, status, Request
from services.project_service import ProjectsService
from services.service import create_services, Service
from fastapi.responses import Response
from fastapi.exceptions import HTTPException
import permissions


def get_projects_service(services: Service = Depends(create_services)):
    return services.projects


router = APIRouter()


@router.get("/projects/{project_id}", response_model=ProjectSchema)
async def get_project(
    project_id: int,
    service: ProjectsService = Depends(get_projects_service),
    base_project=Depends(permissions.ProjectChecker(is_admin=True, is_active=True)),
):
    project = await service.get_by_id(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Проект не найден")
    return project


@router.get("/projects", response_model=list[ProjectSchema])
async def get_all_projects(
    service: ProjectsService = Depends(get_projects_service),
    base_project=Depends(permissions.ProjectChecker(is_admin=True, is_active=True)),
):
    return await service.get_all()


@router.post("/projects", response_model=ProjectSchema)
async def create_project(
    project: ProjectCreateSchema,
    service: ProjectsService = Depends(get_projects_service),
):
    return await service.create(project)


@router.patch("/projects/{project_id}", response_model=ProjectSchema)
async def patch_project(
    project_id: int,
    project_data: ProjectUpdateSchema,
    service: ProjectsService = Depends(get_projects_service),
    base_project=Depends(permissions.ProjectChecker(is_admin=True, is_active=True)),
):

    project = await service.get_by_id(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Проект не найден")

    updated_data = project_data.model_dump(exclude_unset=True)
    for field, value in updated_data.items():
        setattr(project, field, value)

    updated_project = await service.update(project_id, project)
    return updated_project


@router.put("/projects/{project_id}", response_model=ProjectSchema)
async def update_project(
    project_id: int,
    project: ProjectSchema,
    service: ProjectsService = Depends(get_projects_service),
    base_project=Depends(permissions.ProjectChecker(is_admin=True, is_active=True)),
):
    project = await service.update(project_id, project)
    if not project:
        raise HTTPException(status_code=404, detail="Проект не найден")
    return project


@router.delete("/projects/{project_id}")
async def delete_project(
    project_id: int,
    service: ProjectsService = Depends(get_projects_service),
    base_project=Depends(permissions.ProjectChecker(is_admin=True, is_active=True)),
):
    if not await service.get_by_id(project_id):
        raise HTTPException(status_code=404, detail="Проект не найден")
    await service.delete(project_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get("/me", response_model=ProjectWithoutRefreshSchema)
async def get_me(request: Request, base_project=Depends(permissions.ProjectChecker(is_active=True))):
    project = request.state.project
    return project