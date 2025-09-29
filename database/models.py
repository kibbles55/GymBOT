from datetime import datetime
from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey, String, JSON
from sqlalchemy.orm import relationship
from database.database import Base, utc_now



class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer, unique=True, nullable=False)
    height = Column(Integer, nullable=True)
    weight = Column(Float, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    weights = relationship("WeightLog", back_populates="user")
    exercises = relationship("UserExercise", back_populates="user")
    plans = relationship("UserPlan", back_populates="user")

class WeightLog(Base):
    __tablename__ = "weight_logs"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    weight = Column(Float, nullable=False)
    date = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="weights")


class Exercise(Base):
    __tablename__ = "exercise"

    id = Column(Integer, primary_key=True)
    muscle_id = Column(Integer, ForeignKey("muscle_groups.id"), nullable=False)
    name = Column(String, nullable=False)

    muscle = relationship("MuscleGroup", back_populates="exercises")


class MuscleGroup(Base):
    __tablename__ = "muscle_groups"

    id = Column(Integer, primary_key=True)
    group_name = Column(String, nullable=False)

    exercises = relationship("Exercise", back_populates="muscle")


class UserExercise(Base):
    __tablename__ = "user_exercises"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    muscle_id = Column(Integer, ForeignKey("muscle_groups.id"), nullable=False)
    name = Column(String(100), nullable=False)

    user = relationship("User", back_populates="exercises")
    muscle = relationship("MuscleGroup")


class UserPlan(Base):
    __tablename__ = "user_plans"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    plan_name = Column(String, nullable=False)
    exercises = Column(JSON, default=[])

    user = relationship("User", back_populates="plans")

