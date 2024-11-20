from fastapi.testclient import TestClient
from sqlmodel import Session

from app.models import Plan, PlanCreate


def create_test_plan(session: Session) -> Plan:
    plan = Plan(name="Test Plan", price=99.99, description="Test Description")
    session.add(plan)
    session.commit()
    session.refresh(plan)
    return plan


def test_create_plan(client: TestClient, session: Session):
    plan_data = PlanCreate(
        name="Premium Plan", price=199.99, description="Premium features"
    )
    response = client.post("/plans/", json=plan_data.model_dump())
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Premium Plan"
    assert data["price"] == 199.99
    assert data["description"] == "Premium features"
    assert "id" in data


def test_get_plans(client: TestClient, session: Session):
    plan = create_test_plan(session)
    response = client.get("/plans/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["id"] == plan.id
    assert data[0]["name"] == plan.name


def test_get_plan(client: TestClient, session: Session):
    plan = create_test_plan(session)
    response = client.get(f"/plans/{plan.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == plan.id
    assert data["name"] == plan.name


def test_update_plan(client: TestClient, session: Session):
    plan = create_test_plan(session)
    update_data = {"name": "Updated Plan"}
    response = client.patch(f"/plans/{plan.id}", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Updated Plan"


def test_delete_plan(client: TestClient, session: Session):
    plan = create_test_plan(session)
    response = client.delete(f"/plans/{plan.id}")
    assert response.status_code == 204

    # Verify plan is deleted
    response = client.get(f"/plans/{plan.id}")
    assert response.status_code == 404


def test_get_non_existent_plan(client: TestClient):
    response = client.get("/plans/999")
    assert response.status_code == 404


def test_update_non_existent_plan(client: TestClient):
    response = client.patch("/plans/999", json={"name": "New Plan"})
    assert response.status_code == 404


def test_delete_non_existent_plan(client: TestClient):
    response = client.delete("/plans/999")
    assert response.status_code == 404
