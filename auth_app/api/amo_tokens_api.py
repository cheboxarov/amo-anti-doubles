from loguru import logger
from httpx import AsyncClient, Response
from config import INSTALL_WIDET


def validate_amo_response(func):
    async def wrapper(*args, **kwargs):
        response: Response = await func(*args, **kwargs)
        try:
            response.raise_for_status()
        except:
            if response.headers.get("Content-Type", "").startswith("application/json"):
                logger.error(f"bad answer from amo {response.json()}")
            else:
                logger.error(
                    f"bad answer from amo with non-JSON content: {response.text}"
                )
            logger.error(f"bad request: {response.request.body}")
            raise
        return response.json()

    return wrapper


class AmoTokensApi:

    @staticmethod
    @validate_amo_response
    async def get_tokens_by_code(
        client_id: str, client_secret: str, code: str, subdomain: str
    ) -> dict[str, str]:
        url = f"https://{subdomain}.amocrm.ru/oauth2/access_token"
        body = {
            "client_id": client_id,
            "client_secret": client_secret,
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": INSTALL_WIDET,
        }
        async with AsyncClient() as client:
            response = await client.post(url, json=body)
        return response

    @staticmethod
    @validate_amo_response
    async def get_tokens_by_refresh(
        client_id: str, client_secret: str, refresh_token: str, subdomain: str
    ) -> dict[str, str]:
        url = f"https://{subdomain}.amocrm.ru/oauth2/access_token"
        body = {
            "client_id": client_id,
            "client_secret": client_secret,
            "grant_type": "refresh_token",
            "refresh_token": refresh_token,
            "redirect_uri": "https://apps.widgets-tema.ru/amo-roistat-fix/install/",
        }
        async with AsyncClient() as client:
            response = await client.post(url, json=body)
        return response
