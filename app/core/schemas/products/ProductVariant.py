from typing import Optional
from pydantic import BaseModel, Field

class ProductVariantCreateSchema(BaseModel):
    product_id: int
    size_id: int
    color_id: int
    stock_quantity: int = Field(default=0, ge=0)

class ProductVariantResponseSchema(BaseModel):
    id: int = Field(default_factory=int, gt=0)
    product_id: int
    size_id: int
    color_id: int
    stock_quantity: int = Field(default=0, ge=0)

class ProductVariantPartialUpdateSchema(BaseModel):
    product_id: Optional[int] = Field(default=None, gt=0)
    size_id: Optional[int] = Field(default=None, gt=0)
    color_id: Optional[int] = Field(default=None, gt=0)
    stock_quantity: Optional[int] = Field(default=None, gt=0)