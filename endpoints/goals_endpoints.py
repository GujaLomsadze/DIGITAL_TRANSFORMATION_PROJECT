from typing import List

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from models.all_models import GoalCreate, Goal, GoalBase, GoalUpdate
from utils.db import get_db

router = APIRouter()


@router.post("/goals/", response_model=GoalCreate)
def create_goal(goal: GoalCreate, db: Session = Depends(get_db)):
    db_goal = Goal(**goal.dict())
    db.add(db_goal)
    db.commit()
    db.refresh(db_goal)
    db.close()
    return db_goal


@router.get("/goals/{goal_id}", response_model=GoalBase)
def read_goal(goal_id: int, db: Session = Depends(get_db)):
    db_goal = db.query(Goal).filter(Goal.id == goal_id).first()
    db.close()
    if db_goal is None:
        raise HTTPException(status_code=404, detail="Goal not found")
    return db_goal


@router.get("/goals/", response_model=List[GoalBase])
def read_goals(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    goals = db.query(Goal).offset(skip).limit(limit).all()
    db.close()
    return goals


@router.put("/goals/{goal_id}", response_model=GoalBase)
def update_goal(goal_id: int, goal: GoalUpdate, db: Session = Depends(get_db)):
    db_goal = db.query(Goal).filter(Goal.id == goal_id).first()
    if db_goal is None:
        db.close()
        raise HTTPException(status_code=404, detail="Goal not found")
    for key, value in goal.dict().items():
        setattr(db_goal, key, value)
    db.commit()
    db.refresh(db_goal)
    db.close()
    return db_goal


@router.delete("/goals/{goal_id}", response_model=GoalBase)
def delete_goal(goal_id: int, db: Session = Depends(get_db)):
    db_goal = db.query(Goal).filter(Goal.id == goal_id).first()
    if db_goal is None:
        db.close()
        raise HTTPException(status_code=404, detail="Goal not found")
    db.delete(db_goal)
    db.commit()
    db.close()
    return db_goal
