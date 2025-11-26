import pytest
import pytest_asyncio


@pytest_asyncio.fixture()
async def order_item_payload(order_factory, product_variant_factory, faker):
    order = await order_factory()
    variant = await product_variant_factory()
    return {
        "order_id": order.id,
        "product_variant_id": variant.id,
        "quantity": faker.random_int(min=1, max=5),
        "price_at_order": float(faker.pydecimal(left_digits=3, right_digits=2, positive=True)),
    }


@pytest.mark.asyncio
async def test_create_order_item(client, order_item_payload):
    response = await client.post("/api/order_items/", json=order_item_payload)
    assert response.status_code == 201
    data = response.json()
    assert data["order_id"] == order_item_payload["order_id"]
    assert data["product_variant_id"] == order_item_payload["product_variant_id"]
    assert data["quantity"] == order_item_payload["quantity"]
    assert float(data["price_at_order"]) == order_item_payload["price_at_order"]


@pytest.mark.asyncio
async def test_get_order_item(client, order_item_factory):
    order_item = await order_item_factory()
    response = await client.get(f"/api/order_items/{order_item.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == order_item.id
    assert data["order_id"] == order_item.order_id
    assert data["product_variant_id"] == order_item.product_variant_id
    assert data["quantity"] == order_item.quantity
    assert float(data["price_at_order"]) == float(order_item.price_at_order)


@pytest.mark.asyncio
async def test_get_order_items(client, order_item_factory):
    await order_item_factory()
    await order_item_factory()
    await order_item_factory()

    response = await client.get("/api/order_items/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 3


@pytest.mark.asyncio
async def test_update_order_item(client, order_item_factory, order_factory, product_variant_factory):
    order_item = await order_item_factory()
    new_order = await order_factory()
    new_variant = await product_variant_factory()

    updated_payload = {
        "order_id": new_order.id,
        "product_variant_id": new_variant.id,
        "quantity": 10,
        "price_at_order": 150.00,
    }
    response = await client.put(f"/api/order_items/{order_item.id}", json=updated_payload)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == order_item.id
    assert data["order_id"] == updated_payload["order_id"]
    assert data["product_variant_id"] == updated_payload["product_variant_id"]
    assert data["quantity"] == updated_payload["quantity"]
    assert float(data["price_at_order"]) == updated_payload["price_at_order"]


@pytest.mark.asyncio
async def test_partial_update_order_item(client, order_item_factory):
    order_item = await order_item_factory()
    partial_payload = {
        "quantity": 7,
    }
    response = await client.patch(f"/api/order_items/{order_item.id}", json=partial_payload)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == order_item.id
    assert data["quantity"] == partial_payload["quantity"]
    assert data["order_id"] == order_item.order_id


@pytest.mark.asyncio
async def test_delete_order_item(client, order_item_factory, auth_headers):
    order_item = await order_item_factory()
    response = await client.delete(f"/api/order_items/{order_item.id}", headers=auth_headers)
    assert response.status_code == 204


@pytest.mark.asyncio
async def test_delete_order_item_unauthorized(client, order_item_factory):
    order_item = await order_item_factory()
    response = await client.delete(f"/api/order_items/{order_item.id}")
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_get_nonexistent_order_item(client):
    response = await client.get("/api/order_items/9999")
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Order item not found"