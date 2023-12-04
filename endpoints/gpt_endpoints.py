import openai
from fastapi import Depends
from fastapi import HTTPException, Body, APIRouter
from sqlalchemy.orm import Session

from configs.load_config import get_config
from models.all_models import User, LearningStyle, Conversation
from utils.db import get_db

router = APIRouter()
_, openai_conf, _ = get_config()


@router.post("/ask_gpt/")
async def ask_gpt(
        message: str = Body(..., embed=True),
        pre_message: str = Body(None, embed=True),
        user_id: str = Body(..., embed=True),
        db: Session = Depends(get_db)
):
    """
    Endpoint which receives pre_message information, such as demographics, sends 'question' to ChatGPT
    and returns response

    :param db: Database session (Connection)
    :param message: User message
    :param pre_message: User pre-message (Demographics or etc.)
    :param user_id: Unique user ID for the customer (user)
    :return: Json with response and question asked
    """
    # Fetch user data from the database
    user_data = db.query(User).filter(User.id == user_id).first()
    if not user_data:
        raise HTTPException(status_code=404, detail="User not found")
    learning_style = db.query(LearningStyle).filter(LearningStyle.id == user_data.learning_style_id).first()
    if not learning_style:
        raise HTTPException(status_code=404, detail="Learning style not found for user")

    # Format demographic info
    demographic_info = f"""
    My name is: {user_data.name}
    My age is: {user_data.age}
    My gender is: {user_data.gender}
    My study program (major) is: {user_data.course_program_study}
    My employment status is: {user_data.employment_status}
    My civil status is: {user_data.civil_status}
    My Learning Style is: {learning_style.learning_style_name}. {learning_style.description}.
    
    """

    full_message = demographic_info

    if pre_message:
        if pre_message[-1] != ".":
            pre_message += "."
        pre_message += "\n"

        full_message += pre_message

    full_message += message

    response = openai.Completion.create(engine=openai_conf["engine"], prompt=full_message, max_tokens=150)
    answer = response.choices[0].text.strip()

    # Save the conversation to the database
    conversation = Conversation(user_id=user_id, user_question=full_message, gpt_answer=answer)
    db.add(conversation)
    db.commit()

    return {"chagpt_answer": answer, "question": message, "full_message": full_message}
