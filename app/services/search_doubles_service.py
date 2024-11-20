from app.schemas.doubles_schemas import DoubleEntityResponse
from py_amo.async_repositories import (
    BaseAsyncRepository,
    ContactsAsyncRepository,
    CompaniesAsyncRepository,
)
from py_amo.services import AsyncAmoSession
from app.schemas.doubles_schemas import FieldName


class FindDoublesService:

    def __init__(self, repository: BaseAsyncRepository, session: AsyncAmoSession):
        self.repository = repository
        self.session = session

    async def find_doubles(self, field_names: list[str]):
        entities_count = None
        if isinstance(self.repository, ContactsAsyncRepository):
            entities_count = await self.session.contacts.count()
        elif isinstance(self.repository, CompaniesAsyncRepository):
            entities_count = await self.session.companies.count()
        else:
            raise ValueError("Bad repository")
        entities = await self.repository.get_all(limit=entities_count)
        finded_entities: dict[str, list] = {}
        for entity in entities:
            assert hasattr(entity, "custom_fields_values")
            try:
                for cf in entity.custom_fields_values:
                    if (field_name := cf.field_name) in field_names:
                        value = cf.values[0].value
                        if field_name == FieldName.phone:
                            value = (
                                value.replace("+", "")
                                .replace("-", "")
                                .replace(" ", "")
                                .replace("(", "")
                                .replace(")", "")[1:]
                            )
                            if not value.isdigit():
                                continue
                        if field_name == FieldName.email and not "@" in value:
                            continue
                        if finded_entities.get(value) is None:
                            finded_entities[value] = [
                                DoubleEntityResponse(**entity.model_dump())
                            ]
                        elif entity.id not in [
                            account.id for account in finded_entities.get(value)
                        ]:
                            finded_entities[value].append(
                                DoubleEntityResponse(**entity.model_dump())
                            )
            except Exception:
                pass
        doubles = {}
        for value, accounts in finded_entities.items():
            if len(accounts) > 1:
                doubles[value] = accounts
        return doubles
