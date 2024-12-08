from schemas.widget_schema import WidgetSchema, WidgetCreateSchema, WidgetUpdateSchema
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from services.widgets_service import WidgetsService
from services.services_factory import create_services_factory, ServicesFactory
from fastapi.responses import Response


def get_widgets_service(services: ServicesFactory = Depends(create_services_factory)):
    return services.widgets


router = APIRouter()


@router.get("/widgets/{widget_id}", response_model=WidgetSchema)
async def get_widget(
    widget_id: int, service: WidgetsService = Depends(get_widgets_service)
):
    """
    Get a widget by id.

    Args:
        widget_id: The id of the widget to be retrieved.

    Returns:
        A widget with the given id.

    Raises:
        HTTPException: If the widget with given id does not exist.
    """
    widget = await service.get_by_id(widget_id)
    if not widget:
        raise HTTPException(status_code=404, detail="Виджет не найден")
    return widget


@router.get("/widgets", response_model=List[WidgetSchema])
async def get_all_widgets(service: WidgetsService = Depends(get_widgets_service)):
    """
    Get all widgets.

    Args:
        service: The service used to get all widgets.

    Returns:
        A list of all widgets.
    """
    return await service.get_all()


@router.post(
    "/widgets", response_model=WidgetSchema, status_code=status.HTTP_201_CREATED
)
async def create_widget(
    widget: WidgetCreateSchema, service: WidgetsService = Depends(get_widgets_service)
):
    """
    Create a new widget.

    Args:
        widget (WidgetCreateSchema): The widget to be created.

    Returns:
        WidgetSchema: The created widget.
    """
    return await service.create(widget)


@router.put("/widgets/{widget_id}", response_model=WidgetSchema)
async def update_widget(
    widget_id: int,
    widget: WidgetUpdateSchema,
    service: WidgetsService = Depends(get_widgets_service),
):
    """
    Update an existing widget.

    Args:
        widget_id (int): The id of the widget to be updated.
        widget (WidgetUpdateSchema): The widget data to update.

    Returns:
        WidgetSchema: The updated widget.

    Raises:
        HTTPException: If the widget with given id does not exist.
    """
    existing_widget = await service.get_by_id(widget_id)
    if not existing_widget:
        raise HTTPException(status_code=404, detail="Виджет не найден")
    return await service.update(widget_id, widget)


@router.delete("/widgets/{widget_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_widget(
    widget_id: int, service: WidgetsService = Depends(get_widgets_service)
):
    """
    Delete a widget by id.

    Args:
        widget_id (int): The id of the widget to be deleted.

    Raises:
        HTTPException: If the widget with given id does not exist.

    Returns:
        Response: A response with status code 204 indicating successful deletion.
    """
    existing_widget = await service.get_by_id(widget_id)
    if not existing_widget:
        raise HTTPException(status_code=404, detail="Виджет не найден")

    await service.delete(widget_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
