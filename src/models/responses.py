from typing import List, TypeVar, Generic
from pydantic import BaseModel

Item = TypeVar("Item")


class PaginatedResponse(BaseModel, Generic[Item]):
    items: List[Item]
    total: int
    page: int = 1
    per_page: int = 25


class ErrorMessage(BaseModel):
    detail: str
