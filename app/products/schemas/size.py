from typing import Optional
from pydantic import BaseModel, Field


class SizeCreateSchema(BaseModel):
    label: str = Field(max_length=10)


class SizeResponseSchema(BaseModel):
    id: int = Field(default_factory=int, gt=0)
    label: str


class SizePartialUpdateSchema(BaseModel):
    label: Optional[str] = Field(default=None, max_length=10)