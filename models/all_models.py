from datetime import date
from enum import Enum
from typing import Optional, List, Dict, Any

from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, CheckConstraint, DateTime, func
from sqlalchemy import Date, Text
from sqlalchemy import Enum as SQLAlchemyEnum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class GenderEnum(str, Enum):
    male = "male"
    female = "female"
    other = "other"
    undisclosed = "undisclosed"


class EmploymentStatusEnum(str, Enum):
    full_time = "full_time"
    part_time = "part_time"
    unemployed = "unemployed"


class CivilStatusEnum(str, Enum):
    single = "single"
    married = "married"


class UserBase(BaseModel):
    name: str
    middle_name: str
    lastname: str
    age: int
    gender: GenderEnum
    course_program_study: str
    email_address: str
    employment_status: EmploymentStatusEnum
    civil_status: CivilStatusEnum
    has_kids: bool
    learning_style_id: int


class UserBaseWithID(BaseModel):
    id: int
    name: str
    middle_name: str
    lastname: str
    age: int
    gender: GenderEnum
    course_program_study: str
    email_address: str
    employment_status: EmploymentStatusEnum
    civil_status: CivilStatusEnum
    has_kids: bool
    learning_style_id: int


class UserCreate(UserBase):
    # All fields are required when creating a user
    pass


class UserUpdate(BaseModel):
    name: Optional[str]
    age: Optional[int]
    gender: Optional[GenderEnum]
    course_program_study: Optional[str]
    email_address: Optional[str]
    employment_status: Optional[EmploymentStatusEnum]
    civil_status: Optional[CivilStatusEnum]
    has_kids: Optional[bool]
    learning_style_id: Optional[int]


class UserResponse(UserBase):
    id: int


class UsersResponse(BaseModel):
    users: Dict[Any, List[UserBase]]


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    middle_name = Column(String, index=True)
    lastname = Column(String, index=True)
    age = Column(Integer)
    gender = Column(SQLAlchemyEnum(GenderEnum))
    course_program_study = Column(String)
    email_address = Column(String, unique=True, index=True)
    employment_status = Column(SQLAlchemyEnum(EmploymentStatusEnum), default="unemployed")
    civil_status = Column(SQLAlchemyEnum(CivilStatusEnum), default="single")
    has_kids = Column(Boolean, default=False)
    learning_style_id = Column(Integer)  # Assuming this relates to another table

    def json(self):
        return {"id": self.id,
                "name": self.name,
                "middle_name": self.middle_name,
                "lastname": self.lastname,
                "age": self.age,
                "gender": self.gender,
                "course_program_study": self.course_program_study,
                "email_address": self.email_address,
                "employment_status": self.employment_status,
                "civil_status": self.civil_status,
                "has_kids": self.has_kids,
                "learning_style_id": self.learning_style_id}


class LearningStyle(Base):
    __tablename__ = "learning_styles"

    id = Column(Integer, primary_key=True, index=True)
    learning_style_name = Column(String, index=True)
    description = Column(String)


class Goal(Base):
    __tablename__ = "goals"
    id = Column(Integer, primary_key=True, index=True)
    goal_name = Column(String(255), nullable=False)
    goal_description = Column(Text)
    goal_owner = Column(Integer, ForeignKey('users.id'))
    start_date = Column(DateTime(timezone=True))
    end_date = Column(DateTime(timezone=True))
    goal_category = Column(String(255))
    status = Column(String(50),
                    CheckConstraint("status IN ('to-do', 'in-progress', 'finished', 'blocked', 'cancelled')"))
    tasks_entry_id = Column(Integer, ForeignKey('tasks.tasks_entry_id'), nullable=True)

    # Relationship with the Task class
    tasks = relationship("Task", back_populates="goal")


class GoalCreate(BaseModel):
    goal_name: str
    goal_description: Optional[str] = None
    goal_owner: int
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    goal_category: Optional[str] = None
    status: str
    tasks_entry_id: Optional[int]


class GoalUpdate(BaseModel):
    goal_name: Optional[str] = None
    goal_description: Optional[str] = None
    goal_owner: Optional[int] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    goal_category: Optional[str] = None
    status: Optional[str] = None
    tasks_entry_id: Optional[int] = None


class GoalBase(BaseModel):
    id: int
    goal_name: str
    goal_description: Optional[str]
    goal_owner: int
    start_date: Optional[date]
    end_date: Optional[date]
    goal_category: Optional[str]
    status: str
    tasks_entry_id: Optional[int]


class Task(Base):
    __tablename__ = 'tasks'

    tasks_entry_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    start_date = Column(String)
    end_date = Column(String)
    category = Column(String(255))
    status = Column(String(50), CheckConstraint("status IN ('to-do', 'in-progress', 'finished', 'blocked')"))

    # Relationship with the Goal class
    goal = relationship("Goal", back_populates="tasks")


class Conversation(Base):
    __tablename__ = 'conversations'

    conversation_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    user_question = Column(Text, nullable=False)
    gpt_answer = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=func.current_timestamp())


class ConversationBase(BaseModel):
    conversation_id: int
    user_id: int
    user_question: str
    gpt_answer: str
    timestamp: date
