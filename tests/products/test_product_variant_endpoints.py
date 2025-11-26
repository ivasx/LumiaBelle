import pytest


@pytest.fixture()
async def variant_payload(product_factory, size_factory, color_factory, faker):
    product = await product_factory()
    size = await size_factory()
    color = await color_factory()
    return {
        "product_id": product.id,
        "size_id": size.id,
        "color_id": color.id,
        "stock_quantity": faker.random_int(min=0, max=100),
    }


@pytest.mark.asyncio
async def test_create_product_variant(client, variant_payload):
    response = await client.post("/api/product_variants/", json=variant_payload)
    assert response.status_code == 201
    data = response.json()
    assert data["product_id"] == variant_payload["product_id"]
    assert data["size_id"] == variant_payload["size_id"]
    assert data["color_id"] == variant_payload["color_id"]
    assert data["stock_quantity"] == variant_payload["stock_quantity"]


@pytest.mark.asyncio
async def test_get_product_variant(client, product_variant_factory):
    variant = await product_variant_factory()
    response = await client.get(f"/api/product_variants/{variant.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == variant.id
    assert data["product_id"] == variant.product_id
    assert data["size_id"] == variant.size_id
    assert data["color_id"] == variant.color_id
    assert data["stock_quantity"] == variant.stock_quantity


@pytest.mark.asyncio
async def test_get_product_variants(client, product_variant_factory):
    await product_variant_factory()
    await product_variant_factory()
    await product_variant_factory()

    response = await client.get("/api/product_variants/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 3


@pytest.mark.asyncio
async def test_update_product_variant(client, product_variant_factory, product_factory, size_factory, color_factory):
    variant = await product_variant_factory()
    new_product = await product_factory()
    new_size = await size_factory()
    new_color = await color_factory()

    updated_payload = {
        "product_id": new_product.id,
        "size_id": new_size.id,
        "color_id": new_color.id,
        "stock_quantity": 50,
    }
    response = await client.put(f"/api/product_variants/{variant.id}", json=updated_payload)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == variant.id
    assert data["product_id"] == updated_payload["product_id"]
    assert data["size_id"] == updated_payload["size_id"]
    assert data["color_id"] == updated_payload["color_id"]
    assert data["stock_quantity"] == updated_payload["stock_quantity"]


@pytest.mark.asyncio
async def test_partial_update_product_variant(client, product_variant_factory):
    variant = await product_variant_factory()
    partial_payload = {
        "stock_quantity": 75,
    }
    response = await client.patch(f"/api/product_variants/{variant.id}", json=partial_payload)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == variant.id
    assert data["stock_quantity"] == partial_payload["stock_quantity"]
    assert data["product_id"] == variant.product_id


@pytest.mark.asyncio
async def test_delete_product_variant(client, product_variant_factory, auth_headers):
    variant = await product_variant_factory()
    response = await client.delete(f"/api/product_variants/{variant.id}", headers=auth_headers)
    assert response.status_code == 204


@pytest.mark.asyncio
async def test_delete_product_variant_unauthorized(client, product_variant_factory):
    variant = await product_variant_factory()
    response = await client.delete(f"/api/product_variants/{variant.id}")
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_get_nonexistent_product_variant(client):
    response = await client.get("/api/product_variants/9999")
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Product variant not found"