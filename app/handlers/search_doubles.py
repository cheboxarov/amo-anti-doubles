from fastapi import APIRouter, Request
from schemas import GetDoublesRequest, DoubleEntityResponse
from py_amo.services import AsyncAmoSession

router = APIRouter()

@router.post("/get_doubles/{subdomain}")
async def search_doubles(request_data: GetDoublesRequest, subdomain: str, request: Request):
    
    session = AsyncAmoSession(request.state.token, subdomain)
    if request_data.entity_type == "contacts" and request_data.search_type == "phone":
        doubles = await find_doubles_by_phone_number(session)
    return doubles


async def find_doubles_by_phone_number(session):
    contacts_count = await session.contacts.count()
    contacts = await session.contacts.get_all(limit=contacts_count)
    phones: dict[str, list] = {}
    for contact in contacts:
        try:
            for cf in contact.custom_fields_values:
                if cf.field_name == "Телефон":
                    phone = cf.values[0].value
                    phone = (
                        phone.replace("+", "")
                        .replace("-", "")
                        .replace(" ", "")
                        .replace("(", "")
                        .replace(")", "")[1:]
                    )
                    if phones.get(phone) is None:
                        phones[phone] = [DoubleEntityResponse(**contact.dict())]
                    elif contact.id not in [account.id for account in phones.get(phone)]:
                        phones[phone].append(DoubleEntityResponse(**contact.dict()))
        except Exception as error:
            pass
    doubles = {}
    for phone, accounts in phones.items():
        if len(accounts) > 1:
            doubles[phone] = accounts
    return doubles
