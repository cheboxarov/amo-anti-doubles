from pydantic import BaseModel
from enum import Enum


class EntityType(str, Enum):
    contacts = "contacts"
    companies = "companies"


class FieldName(str, Enum):
    phone = "Телефон"
    email = "Email"


class SearchType(str, Enum):
    phone = "phone"
    email = "email"


FIELD_NAME_TO_SEARCH_TYPE = {
    SearchType.phone: FieldName.phone,
    SearchType.email: FieldName.email,
}


class GetDoublesRequest(BaseModel):
    entity_type: EntityType
    search_type: SearchType


class DoubleEntityResponse(BaseModel):
    id: int
    name: str
