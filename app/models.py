from enum import Enum

from pydantic import BaseModel, EmailStr
from sqlmodel import Field, Relationship, SQLModel


# --- CustomerPlan ---
class StatusEnum(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"


class CustomerPlan(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    plan_id: int = Field(foreign_key="plan.id")
    customer_id: int = Field(foreign_key="customer.id")
    status: StatusEnum = Field(default=StatusEnum.ACTIVE)


# --- Plan ---


class PlanBase(SQLModel):
    name: str = Field(...)
    price: float = Field(...)
    description: str = Field(...)


class Plan(PlanBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    customers: list["Customer"] = Relationship(
        back_populates="plans", link_model=CustomerPlan
    )


class PlanCreate(PlanBase):
    pass


class PlanUpdate(SQLModel):
    name: str | None = None
    price: float | None = None
    description: str | None = None


class PlanPublic(PlanBase):
    id: int


# --- Customer ---


class CustomerBase(SQLModel):
    name: str = Field(...)
    description: str | None = Field(None)
    email: EmailStr = Field(..., unique=True)
    age: int | None = Field(None)


class CustomerCreate(CustomerBase):
    pass


class CustomerUpdate(SQLModel):
    name: str | None = None
    description: str | None = None
    email: EmailStr | None = None
    age: int | None = None


class Customer(CustomerBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    transactions: list["Transaction"] = Relationship(back_populates="customer")
    plans: list[Plan] = Relationship(
        back_populates="customers", link_model=CustomerPlan
    )


class CustomerPublic(CustomerBase):
    id: int


# --- Transaction and Invoice ---


class TransactionBase(SQLModel):
    amount: float = Field(...)
    description: str | None = Field(None)

    customer_id: int = Field(foreign_key="customer.id")


class TransactionCreate(TransactionBase):
    pass


class TransactionUpdate(SQLModel):
    amount: float | None = None
    description: str | None = None

    customer_id: int | None = None


class Transaction(TransactionBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    customer: Customer = Relationship(back_populates="transactions")


class TransactionPublic(TransactionBase):
    id: int


class InvoiceBase(BaseModel):
    id: int
    customer: Customer
    transactions: list[Transaction]
    total: float

    @property
    def amount_total(self):
        return sum([transaction.amount for transaction in self.transactions])
