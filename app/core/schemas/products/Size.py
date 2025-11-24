from typing import Optional
from pydantic import BaseModel, Field


class ColorCreateSchema(BaseModel):
    label: str = Field(max_length=10)


class ColorResponseSchema(BaseModel):
    id: int = Field(default_factory=int, gt=0)
    label: str



class ColorPartialUpdateSchema(BaseModel):
    label: Optional[str] = Field(default=None, max_length=10)