from typing import List

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from models.all_models import User, UserBase, UserCreate, UserResponse, UserUpdate, UserBaseWithID
from utils.db import get_db

router = APIRouter()


@router.post("/users/", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    # TODO: Check if username or unique identifiers already exists
    db_user = User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    db.close()
    return db_user


@router.get("/users/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.get("/users", response_model=List[UserBaseWithID])
def get_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = db.query(User).offset(skip).limit(limit).all()
    return users


@router.patch("/users/{user_id}")
async def update_user(user_id: int, user: UserUpdate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()

    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    for var, value in user.dict().items():
        if value is not None:
            setattr(db_user, var, value)

    db.commit()

    return True


@router.delete("/users/{user_id}", response_model=dict)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(db_user)
    db.commit()
    return {"status": "deleted", "user_id": user_id}
