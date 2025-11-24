from typing import Optional
from pydantic import BaseModel, Field

class CartCreateSchema(BaseModel):
    user_id: int

class CartResponseSchema(BaseModel):
    user_id: int

class CartPartialUpdateSchema(BaseModel):
    user_id: Optional[int] = Field(default=None, gt=0)