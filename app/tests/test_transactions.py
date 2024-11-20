from fastapi.testclient import TestClient
from sqlmodel import Session

from app.models import Transaction, TransactionCreate
from app.tests.test_customers import create_test_customer


def create_test_transaction(session: Session, customer_id: int) -> Transaction:
    transaction = Transaction(
        amount=100.0, description="Test Transaction", customer_id=customer_id
    )
    session.add(transaction)
    session.commit()
    session.refresh(transaction)
    return transaction


def test_create_transaction(client: TestClient, session: Session):
    customer = create_test_customer(session)
    transaction_data = TransactionCreate(
        amount=100.0, description="Test Transaction", customer_id=customer.id
    )
    response = client.post("/transactions/", json=transaction_data.model_dump())
    assert response.status_code == 201
    data = response.json()
    assert data["amount"] == 100.0
    assert data["description"] == "Test Transaction"
    assert data["customer_id"] == customer.id
    assert "id" in data


def test_get_transactions(client: TestClient, session: Session):
    customer = create_test_customer(session)
    transaction = create_test_transaction(session, customer.id)
    response = client.get("/transactions/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["id"] == transaction.id
    assert data[0]["amount"] == transaction.amount


def test_get_transaction(client: TestClient, session: Session):
    customer = create_test_customer(session)
    transaction = create_test_transaction(session, customer.id)
    response = client.get(f"/transactions/{transaction.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == transaction.id
    assert data["amount"] == transaction.amount


def test_update_transaction(client: TestClient, session: Session):
    customer = create_test_customer(session)
    transaction = create_test_transaction(session, customer.id)
    update_data = {"amount": 200.0}
    response = client.patch(f"/transactions/{transaction.id}", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["amount"] == 200.0


def test_delete_transaction(client: TestClient, session: Session):
    customer = create_test_customer(session)
    transaction = create_test_transaction(session, customer.id)
    response = client.delete(f"/transactions/{transaction.id}")
    assert response.status_code == 204

    # Verify transaction is deleted
    response = client.get(f"/transactions/{transaction.id}")
    assert response.status_code == 404


def test_get_non_existent_transaction(client: TestClient):
    response = client.get("/transactions/999")
    assert response.status_code == 404


def test_update_non_existent_transaction(client: TestClient):
    response = client.patch("/transactions/999", json={"amount": 200.0})
    assert response.status_code == 404


def test_delete_non_existent_transaction(client: TestClient):
    response = client.delete("/transactions/999")
    assert response.status_code == 404
