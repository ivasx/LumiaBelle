from decimal import Decimal
from typing import Optional
from pydantic import BaseModel, Field

class ProductCreateSchema(BaseModel):
    title: str = Field(max_length=255)
    description: Optional[str] = None
    price: Decimal = Field(gt=0)
    category_id: int

class ProductResponseSchema(BaseModel):
    id: int = Field(default_factory=int, gt=0)
    title: str
    description: Optional[str] = None
    price: Decimal
    category_id: int

class ProductPartialUpdateSchema(BaseModel):
    title: Optional[str] = Field(default=None, max_length=255)
    description: Optional[str] = Field(default=None)
    price: Optional[Decimal] =Field(default=None, gt=0)