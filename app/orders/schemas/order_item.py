from datetime import datetime
from decimal import Decimal
from typing import Optional
from pydantic import BaseModel, Field


class OrderItemCreateSchema(BaseModel):
    order_id: int = Field(default_factory=int, ge=0)
    product_variant_id: int = Field(default_factory=int, ge=0)
    quantity: int = Field(default=1, gt=0)
    price_at_order: Decimal = Field(gt=0)


class OrderItemResponseSchema(BaseModel):
    id: int = Field(default_factory=int, gt=0)
    order_id: int
    product_variant_id: int
    quantity: int
    price_at_order: Decimal


class OrderItemPartialUpdateSchema(BaseModel):
    order_id: Optional[int] = Field(default=None, ge=0)
    product_variant_id: Optional[int] = Field(default=None, ge=0)
    quantity: Optional[int] = Field(default=None, gt=0)
    price_at_order: Optional[Decimal] = Field(default=None, decimal_places=2, gt=0)