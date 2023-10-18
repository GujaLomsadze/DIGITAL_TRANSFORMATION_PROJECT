from typing import List

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from models.all_models import GoalCreate, Goal, GoalBase, GoalUpdate, Conversation
from utils.db import get_db

router = APIRouter()


@router.get("/conversations/")
async def get_all_conversations(db: Session = Depends(get_db)
                                ):
    conversations = db.query(Conversation).all()
    db.close()
    return {"conversations": [conv.__dict__ for conv in conversations]}


@router.get("/conversations/{user_id}")
async def get_conversation_by_user_id(user_id: int, db: Session = Depends(get_db)
                                      ):
    conversations = db.query(Conversation).filter(Conversation.user_id == user_id).all()
    db.close()
    if not conversations:
        raise HTTPException(status_code=404, detail="Conversations not found")
    return {"conversations": [conv.__dict__ for conv in conversations]}
