from sqlalchemy import Integer, ForeignKey, UniqueConstraint, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.models.base import BaseModel


class CartItem(BaseModel):
    __tablename__ = 'cart_item'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    cart_id: Mapped[int] = mapped_column(
        ForeignKey('cart.id'),
        nullable=False
    )
    product_variant_id: Mapped[int] = mapped_column(
        ForeignKey('product_variant.id'),
        nullable=False
    )
    quantity: Mapped[int] = mapped_column(Integer, nullable=False, default=1)


    cart: Mapped['Cart'] = relationship(back_populates='items')
    variant: Mapped['ProductVariant'] = relationship(back_populates='cart_items')

    __table_args__ = (
        UniqueConstraint('cart_id', 'product_variant_id', name='uq_cart_item_variant'),
        CheckConstraint('quantity > 0', name='check_quantity_positive'),
    )