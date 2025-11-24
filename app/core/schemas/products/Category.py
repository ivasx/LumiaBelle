from typing import Optional
from pydantic import BaseModel, Field


class CategoryCreateSchema(BaseModel):
    name: str = Field(max_length=100)


class CategoryResponseSchema(BaseModel):
    id: int = Field(default_factory=int, gt=0)
    name: str


class CategoryPartialUpdateSchema(BaseModel):
    name: Optional[str] = Field(default=None, max_length=100)