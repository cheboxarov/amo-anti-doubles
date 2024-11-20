from schemas.widget_schema import WidgetSchema
from typing import List
from fastapi import APIRouter, Depends
from services.widgets_service import WidgetsService
from services.service import create_services, Service


def get_widgets_service(services: Service = Depends(create_services)):
    return services.widgets


router = APIRouter()


@router.get("/widgets/{widget_id}", response_model=WidgetSchema)
async def get_widget(
    widget_id: int, service: WidgetsService = Depends(get_widgets_service)
):
    return await service.get_by_id(widget_id)


@router.get("/widgets", response_model=list[WidgetSchema])
async def get_all_widgets(service: WidgetsService = Depends(get_widgets_service)):
    return await service.get_all()


@router.post("/widgets", response_model=WidgetSchema)
async def create_widget(
    widget: WidgetSchema, service: WidgetsService = Depends(get_widgets_service)
):
    return await service.create(widget)


@router.put("/widgets/{widget_id}", response_model=WidgetSchema)
async def update_widget(
    widget_id: int,
    widget: WidgetSchema,
    service: WidgetsService = Depends(get_widgets_service),
):
    return await service.update(widget_id, widget)


@router.delete("/widgets/{widget_id}", response_model=bool)
async def delete_widget(
    widget_id: int, service: WidgetsService = Depends(get_widgets_service)
):
    return await service.delete(widget_id)
