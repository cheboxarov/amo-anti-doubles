from fastapi import APIRouter, Depends
from services.service import Service, create_services
from services.auth_service import AuthService
from loguru import logger
import traceback


def get_auth_service(services: Service = Depends(create_services)):
    return services.auth


router = APIRouter()


@router.get("/install")
async def install(
    code: str,
    client_id: str,
    referer: str,
    service: AuthService = Depends(get_auth_service),
):
    """
    Install widget by code and client_id

    :param code: The authorization code
    :param client_id: The client_id of widget
    :param referer: The referer of request. Used for get subdomain.
    :param service: The service for auth
    :return: {"result": "ok"} if install success, else raise error
    """
    try:
        subdomain = referer.split(".")[0]
        service.install_widget(code, client_id, subdomain)
    except Exception as error:
        logger.error(f"Error for install widget {error}")
        logger.error(traceback.format_exc())
    finally:
        return {"result": "ok"}, 200
