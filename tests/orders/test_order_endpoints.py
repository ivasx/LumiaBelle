import pytest
from datetime import datetime


@pytest.fixture()
async def order_payload(user_factory, user_address_factory, faker):
    user = await user_factory()
    address = await user_address_factory(user=user)
    return {
        "user_id": user.id,
        "address_id": address.id,
        "total_amount": float(faker.pydecimal(left_digits=4, right_digits=2, positive=True)),
        "status": "Pending",
        "created_at": datetime.now().isoformat(),
    }


@pytest.mark.asyncio
async def test_create_order(client, order_payload):
    response = await client.post("/api/orders/", json=order_payload)
    assert response.status_code == 201
    data = response.json()
    assert data["user_id"] == order_payload["user_id"]
    assert data["address_id"] == order_payload["address_id"]
    assert float(data["total_amount"]) == order_payload["total_amount"]
    assert data["status"] == order_payload["status"]


@pytest.mark.asyncio
async def test_get_order(client, order_factory):
    order = await order_factory()
    response = await client.get(f"/api/orders/{order.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == order.id
    assert data["user_id"] == order.user_id
    assert data["address_id"] == order.address_id
    assert float(data["total_amount"]) == float(order.total_amount)
    assert data["status"] == order.status


@pytest.mark.asyncio
async def test_get_orders(client, order_factory):
    await order_factory()
    await order_factory()
    await order_factory()

    response = await client.get("/api/orders/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 3


@pytest.mark.asyncio
async def test_update_order(client, order_factory, user_factory, user_address_factory):
    order = await order_factory()
    new_user = await user_factory()
    new_address = await user_address_factory(user=new_user)

    updated_payload = {
        "user_id": new_user.id,
        "address_id": new_address.id,
        "total_amount": 500.00,
        "status": "Shipped",
        "created_at": datetime.now().isoformat(),
    }
    response = await client.put(f"/api/orders/{order.id}", json=updated_payload)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == order.id
    assert data["user_id"] == updated_payload["user_id"]
    assert data["address_id"] == updated_payload["address_id"]
    assert float(data["total_amount"]) == updated_payload["total_amount"]
    assert data["status"] == updated_payload["status"]


@pytest.mark.asyncio
async def test_partial_update_order(client, order_factory):
    order = await order_factory()
    partial_payload = {
        "status": "Delivered",
    }
    response = await client.patch(f"/api/orders/{order.id}", json=partial_payload)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == order.id
    assert data["status"] == partial_payload["status"]
    assert float(data["total_amount"]) == float(order.total_amount)


@pytest.mark.asyncio
async def test_delete_order(client, order_factory, auth_headers):
    order = await order_factory()
    response = await client.delete(f"/api/orders/{order.id}", headers=auth_headers)
    assert response.status_code == 204


@pytest.mark.asyncio
async def test_delete_order_unauthorized(client, order_factory):
    order = await order_factory()
    response = await client.delete(f"/api/orders/{order.id}")
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_get_nonexistent_order(client):
    response = await client.get("/api/orders/9999")
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Order not found"