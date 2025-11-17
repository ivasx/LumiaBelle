from sqlalchemy import Integer, ForeignKey, UniqueConstraint, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.models.base import BaseModel
from typing import List

class ProductVariant(BaseModel):
    __tablename__ = 'product_variant'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    product_id: Mapped[int] = mapped_column(ForeignKey('product.id'), nullable=False)
    size_id: Mapped[int] = mapped_column(ForeignKey('size.id'), nullable=False)
    color_id: Mapped[int] = mapped_column(ForeignKey('color.id'), nullable=False)

    stock_quantity: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    product: Mapped['Product'] = relationship(back_populates='variants')
    size: Mapped['Size'] = relationship()
    color: Mapped['Color'] = relationship()
    cart_items: Mapped[List['CartItem']] = relationship(back_populates='variant')
    __table_args__ = (
        UniqueConstraint('product_id', 'size_id', 'color_id', name='uq_product_variant_combo'),
        CheckConstraint('stock_quantity >= 0', name='check_stock_non_negative'),
    )