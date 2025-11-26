import factory
from app.products.models.category import CategoryModel
from app.products.models.size import SizeModel
from app.products.models.color import ColorModel
from app.products.models.product import ProductModel
from app.products.models.product_variant import ProductVariantModel


class CategoryFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = CategoryModel
        sqlalchemy_session_persistence = "commit"

    name = factory.Faker("word")

class SizeFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = SizeModel
        sqlalchemy_session_persistence = "commit"

    label = factory.Faker("lexify", text="??")


class ColorFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = ColorModel
        sqlalchemy_session_persistence = "commit"

    name = factory.Faker("color_name")
    hex_code = factory.Faker("hex_color")


class ProductFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = ProductModel
        sqlalchemy_session_persistence = "commit"

    title = factory.Faker("sentence", nb_words=3)
    description = factory.Faker("text")
    # Генеруємо Decimal число для ціни
    price = factory.Faker(
        "pydecimal", left_digits=3, right_digits=2, positive=True
    )
    category = factory.SubFactory(CategoryFactory)


class ProductVariantFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = ProductVariantModel
        sqlalchemy_session_persistence = "commit"

    product = factory.SubFactory(ProductFactory)
    size = factory.SubFactory(SizeFactory)
    color = factory.SubFactory(ColorFactory)
    stock_quantity = factory.Faker("random_int", min=0, max=100)