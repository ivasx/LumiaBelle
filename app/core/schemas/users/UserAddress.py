from typing import Optional
from pydantic import BaseModel, Field


class UserAddressCreateSchema(BaseModel):
   user_id: int
   address_line1: str = Field(max_length=255)
   city: str = Field(max_length=100)
   zip_code: str = Field(max_length=10)
   is_default: bool = Field(default=False)

class UserAddressResponseSchema(BaseModel):
    id: int = Field(default_factory=int, gt=0)
    user_id: int
    address_line1: str
    city: str
    zip_code: str
    is_default: bool


class UserAddressPartialUpdateSchema(BaseModel):
    user_id: Optional[int] = Field(default=None, ge=0)
    address_line1: Optional[str] = Field(default=None, max_length=255)
    city: Optional[str] = Field(default=None, max_length=100)
    zip_code: Optional[str] = Field(default=None, max_length=10)
    is_default: Optional[bool] = Field(default=None)
