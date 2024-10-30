from pydantic import BaseModel


class GetDoublesRequest(BaseModel):
    entity_type: str
    search_type: str

class DoubleEntityResponse(BaseModel):
    id: int
    name: str