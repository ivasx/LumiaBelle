import pytest
import pytest_asyncio


@pytest_asyncio.fixture()
async def product_payload(faker, category_factory):
    category = await category_factory()
    return {
        "title": faker.sentence(nb_words=3),
        "description": faker.text(),
        "price": float(faker.pydecimal(left_digits=3, right_digits=2, positive=True)),
        "category_id": category.id,
    }


@pytest.mark.asyncio
async def test_create_product(client, product_payload):
    response = await client.post("/api/products/", json=product_payload)
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == product_payload["title"]
    assert data["description"] == product_payload["description"]
    assert float(data["price"]) == product_payload["price"]
    assert data["category_id"] == product_payload["category_id"]


@pytest.mark.asyncio
async def test_create_product_invalid_category(client, faker):
    invalid_payload = {
        "title": faker.sentence(nb_words=3),
        "description": faker.text(),
        "price": float(faker.pydecimal(left_digits=3, right_digits=2, positive=True)),
        "category_id": 9999,
    }
    response = await client.post("/api/products/", json=invalid_payload)
    assert response.status_code == 400
    data = response.json()
    assert "Invalid category_id" in data["detail"]


@pytest.mark.asyncio
async def test_get_product(client, product_factory):
    product = await product_factory()
    response = await client.get(f"/api/products/{product.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == product.id
    assert data["title"] == product.title
    assert data["description"] == product.description
    assert float(data["price"]) == float(product.price)
    assert data["category_id"] == product.category_id


@pytest.mark.asyncio
async def test_get_products(client, product_factory):
    await product_factory()
    await product_factory()
    await product_factory()

    response = await client.get("/api/products/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 3


@pytest.mark.asyncio
async def test_update_product(client, product_factory, category_factory, faker):
    product = await product_factory()
    new_category = await category_factory()
    updated_payload = {
        "title": "Updated Product Title",
        "description": "Updated description",
        "price": 99.99,
        "category_id": new_category.id,
    }
    response = await client.put(f"/api/products/{product.id}", json=updated_payload)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == product.id
    assert data["title"] == updated_payload["title"]
    assert data["description"] == updated_payload["description"]
    assert float(data["price"]) == updated_payload["price"]
    assert data["category_id"] == updated_payload["category_id"]


@pytest.mark.asyncio
async def test_partial_update_product(client, product_factory):
    product = await product_factory()
    partial_payload = {
        "title": "Partially Updated Title",
    }
    response = await client.patch(f"/api/products/{product.id}", json=partial_payload)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == product.id
    assert data["title"] == partial_payload["title"]
    assert float(data["price"]) == float(product.price)


@pytest.mark.asyncio
async def test_delete_product(client, product_factory, auth_headers):
    product = await product_factory()
    response = await client.delete(f"/api/products/{product.id}", headers=auth_headers)
    assert response.status_code == 204


@pytest.mark.asyncio
async def test_delete_product_unauthorized(client, product_factory):
    product = await product_factory()
    response = await client.delete(f"/api/products/{product.id}")
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_get_nonexistent_product(client):
    response = await client.get("/api/products/9999")
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Product not found"