from typing import Annotated

from fastapi import APIRouter, HTTPException, Query, status
from fastapi.responses import Response
from sqlmodel import select

from app.db import SessionDep
from app.models import (
    Customer,
    CustomerCreate,
    CustomerPlan,
    CustomerPublic,
    CustomerUpdate,
    Plan,
    StatusEnum,
)

router = APIRouter(
    prefix="/customers",
    tags=["Customers"],
)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_customer(
    customer_data: CustomerCreate, session: SessionDep
) -> CustomerPublic:
    customer = Customer.model_validate(customer_data)
    session.add(customer)
    session.commit()
    session.refresh(customer)
    return customer


@router.get("/", response_model=list[CustomerPublic])
async def get_customers(session: SessionDep):
    return session.exec(select(Customer)).all()


@router.get("/{customer_id}")
async def get_customer(customer_id: int, session: SessionDep) -> CustomerPublic:
    customer = session.get(Customer, customer_id)
    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found"
        )
    return customer


@router.patch("/{customer_id}", status_code=status.HTTP_200_OK)
async def update_customer(
    customer_id: int, customer_data: CustomerUpdate, session: SessionDep
) -> CustomerPublic:
    customer = session.get(Customer, customer_id)
    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found"
        )
    customer_data_dict = customer_data.model_dump(exclude_unset=True)
    customer.sqlmodel_update(customer_data_dict)
    session.add(customer)
    session.commit()
    session.refresh(customer)
    return customer


@router.delete("/{customer_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_customer(customer_id: int, session: SessionDep) -> Response:
    customer = session.get(Customer, customer_id)
    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found"
        )
    session.delete(customer)
    session.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post("/{customer_id}/subscribe/{plan_id}", status_code=status.HTTP_201_CREATED)
async def subscribe_customer_to_plan(
    customer_id: int, plan_id: int, session: SessionDep
) -> CustomerPlan:
    customer = session.get(Customer, customer_id)
    plan = session.get(Plan, plan_id)
    if not customer or not plan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer or Plan does not exist",
        )
    customer_plan = CustomerPlan(plan_id=plan.id, customer_id=customer.id)
    session.add(customer_plan)
    session.commit()
    session.refresh(customer_plan)
    return customer_plan


@router.get("/{customer_id}/plans")
async def get_customer_plans(
    customer_id: int, session: SessionDep, plan_status: Annotated[StatusEnum, Query()]
) -> list[CustomerPlan]:
    customer = session.get(Customer, customer_id)
    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found"
        )
    query = (
        select(CustomerPlan)
        .where(CustomerPlan.customer_id == customer_id)
        .where(CustomerPlan.status == plan_status)
    )
    plans = session.exec(query).all()
    return plans
