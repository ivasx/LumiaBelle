from typing import Optional
from pydantic import BaseModel, Field


class ColorCreateSchema(BaseModel):
    name: str = Field(max_length=50)
    hex_code: str = Field(max_length=7)


class ColorResponseSchema(BaseModel):
    id: int = Field(default_factory=int, gt=0)
    name: str
    hex_code: str


class ColorPartialUpdateSchema(BaseModel):
    name: Optional[str] = Field(default=None, max_length=50)
    hex_code: Optional[str] = Field(default=None, max_length=7)