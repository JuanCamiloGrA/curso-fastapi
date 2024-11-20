from typing import Annotated

from fastapi import APIRouter, HTTPException, Query, Response, status
from sqlmodel import select

from app.db import SessionDep
from app.models import (
    Customer,
    Transaction,
    TransactionCreate,
    TransactionPublic,
    TransactionUpdate,
)

router = APIRouter(
    prefix="/transactions",
    tags=["Transactions"],
)


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_transaction(
    transaction_data: TransactionCreate, session: SessionDep
) -> TransactionPublic:
    transaction_data_dict = transaction_data.model_dump()
    customer = session.get(Customer, transaction_data_dict.get("customer_id"))
    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found"
        )
    transaction = Transaction.model_validate(transaction_data)
    session.add(transaction)
    session.commit()
    session.refresh(transaction)
    return transaction


@router.get("")
async def get_transactions(
    session: SessionDep,
    skip: Annotated[int, Query(description="Cantidad de registros a saltar")] = 0,
    limit: Annotated[int, Query(description="Cantidad de registros a mostrar")] = 100,
) -> list[TransactionPublic]:
    query = select(Transaction).offset(skip).limit(limit)
    return session.exec(query).all()


@router.get("/{transaction_id}")
async def get_transaction(
    transaction_id: int, session: SessionDep
) -> TransactionPublic:
    transaction = session.get(Transaction, transaction_id)
    if not transaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Transaction not found"
        )
    return transaction


@router.patch("/{transaction_id}", status_code=status.HTTP_200_OK)
async def update_transaction(
    transaction_id: int, transaction_data: TransactionUpdate, session: SessionDep
) -> TransactionPublic:
    transaction = session.get(Transaction, transaction_id)
    if not transaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Transaction not found"
        )
    transaction_data_dict = transaction_data.model_dump(exclude_unset=True)
    transaction.sqlmodel_update(transaction_data_dict)
    session.add(transaction)
    session.commit()
    session.refresh(transaction)
    return transaction


@router.delete("/{transaction_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_transaction(transaction_id: int, session: SessionDep):
    transaction = session.get(Transaction, transaction_id)
    if not transaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Transaction not found"
        )
    session.delete(transaction)
    session.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
