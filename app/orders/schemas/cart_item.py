from typing import Optional
from pydantic import BaseModel, Field


class CartItemCreateSchema(BaseModel):
    cart_id: int = Field(default_factory=int, ge=0)
    product_variant_id: int = Field(default_factory=int, ge=0)
    quantity: int = Field(default_factory=int, gt=0)


class CartItemResponseSchema(BaseModel):
    id: int = Field(default_factory=int, gt=0)
    cart_id: int
    product_variant_id: int
    quantity: int


class CartItemPartialUpdateSchema(BaseModel):
    cart_id: Optional[int] = Field(default=None, ge=0)
    product_variant_id: Optional[int] = Field(default=None, ge=0)
    quantity: Optional[int] = Field(default=None, gt=0)