from fastapi.testclient import TestClient
from sqlmodel import Session

from app.models import Customer, CustomerCreate, Plan


def create_test_customer(session: Session) -> Customer:
    customer = Customer(name="Test Customer", email="test@example.com")
    session.add(customer)
    session.commit()
    session.refresh(customer)
    return customer


def create_test_plan(session: Session) -> Plan:
    plan = Plan(name="Test Plan", price=99.99, description="Test Description")
    session.add(plan)
    session.commit()
    session.refresh(plan)
    return plan


def test_create_customer(client: TestClient, session: Session):
    customer_data = CustomerCreate(name="John Doe", email="john@example.com")
    response = client.post("/customers/", json=customer_data.model_dump())
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "John Doe"
    assert data["email"] == "john@example.com"
    assert "id" in data


def test_get_customers(client: TestClient, session: Session):
    customer = create_test_customer(session)
    response = client.get("/customers/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["id"] == customer.id
    assert data[0]["name"] == customer.name


def test_get_customer(client: TestClient, session: Session):
    customer = create_test_customer(session)
    response = client.get(f"/customers/{customer.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == customer.id
    assert data["name"] == customer.name


def test_update_customer(client: TestClient, session: Session):
    customer = create_test_customer(session)
    update_data = {"name": "Updated Name"}
    response = client.patch(f"/customers/{customer.id}", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Updated Name"


def test_delete_customer(client: TestClient, session: Session):
    customer = create_test_customer(session)
    response = client.delete(f"/customers/{customer.id}")
    assert response.status_code == 204

    # Verify customer is deleted
    response = client.get(f"/customers/{customer.id}")
    assert response.status_code == 404


def test_subscribe_customer_to_plan(client: TestClient, session: Session):
    customer = create_test_customer(session)
    plan = create_test_plan(session)
    response = client.post(f"/customers/{customer.id}/subscribe/{plan.id}")
    assert response.status_code == 201
    data = response.json()
    assert data["customer_id"] == customer.id
    assert data["plan_id"] == plan.id


def test_get_customer_plans(client: TestClient, session: Session):
    customer = create_test_customer(session)
    plan = create_test_plan(session)
    # First subscribe customer to plan
    client.post(f"/customers/{customer.id}/subscribe/{plan.id}")

    response = client.get(f"/customers/{customer.id}/plans?plan_status=active")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["customer_id"] == customer.id
    assert data[0]["plan_id"] == plan.id


def test_get_non_existent_customer(client: TestClient):
    response = client.get("/customers/999")
    assert response.status_code == 404


def test_update_non_existent_customer(client: TestClient):
    response = client.patch("/customers/999", json={"name": "New Name"})
    assert response.status_code == 404


def test_delete_non_existent_customer(client: TestClient):
    response = client.delete("/customers/999")
    assert response.status_code == 404
