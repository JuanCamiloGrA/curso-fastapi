from fastapi import APIRouter, HTTPException, Response, status
from sqlmodel import select

from app.db import SessionDep
from app.models import Plan, PlanCreate, PlanPublic, PlanUpdate

router = APIRouter(
    prefix="/plans",
    tags=["Plans"],
)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_plan(plan_data: PlanCreate, session: SessionDep) -> PlanPublic:
    plan = Plan.model_validate(plan_data)
    session.add(plan)
    session.commit()
    session.refresh(plan)
    return plan


@router.get("/", response_model=list[PlanPublic])
async def get_plans(session: SessionDep):
    return session.exec(select(Plan)).all()


@router.get("/{plan_id}")
async def get_plan(plan_id: int, session: SessionDep) -> PlanPublic:
    plan = session.get(Plan, plan_id)
    if not plan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Plan not found"
        )
    return plan


@router.patch("/{plan_id}", status_code=status.HTTP_200_OK)
async def update_plan(
    plan_id: int, plan_data: PlanUpdate, session: SessionDep
) -> PlanPublic:
    plan = session.get(Plan, plan_id)
    if not plan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Plan not found"
        )
    plan_data_dict = plan_data.model_dump(exclude_unset=True)
    plan.sqlmodel_update(plan_data_dict)
    session.add(plan)
    session.commit()
    session.refresh(plan)
    return plan


@router.delete("/{plan_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_plan(plan_id: int, session: SessionDep):
    plan = session.get(Plan, plan_id)
    if not plan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Plan not found"
        )
    session.delete(plan)
    session.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
