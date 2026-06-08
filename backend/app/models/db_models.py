from sqlalchemy import Column, Integer, String, ForeignKey , Date , Float
from sqlalchemy.orm import declarative_base , relationship

Base = declarative_base()   

class Users(Base):
    __tablename__ = "users"
    user_id = Column(Integer , primary_key = True)
    username = Column(String, nullable=False)
    email = Column(String, nullable=False)
    password = Column(String,nullable = False)
class MealPlan(Base):
    __tablename__ = "meal_plan"
    plan_id = Column(Integer , primary_key = True)
    user_id = Column(Integer, ForeignKey("users.user_id"))
    num_days = Column(Integer, nullable = False)
    start_date = Column(Date , nullable = False)
    days = relationship("DayPlan", back_populates="meal_plan", cascade="all, delete-orphan")


class DayPlan(Base):
    __tablename__ = "day_plan"
    day_id = Column(Integer , primary_key = True)
    plan_id = Column(Integer, ForeignKey("meal_plan.plan_id"))
    day = Column(String , nullable = False)
    meal_plan = relationship("MealPlan", back_populates="days")
    meals = relationship("Meal" , back_populates = "day",cascade = "all, delete-orphan")

class Meal(Base):
    __tablename__ = "meal"
    meal_id = Column(Integer , primary_key = True)
    day_id = Column(Integer, ForeignKey("day_plan.day_id"))
    name = Column(String, nullable = False)
    calories = Column(Float , nullable = False)
    time_to_cook = Column(Float)
    recipe = Column(String)
    day = relationship("DayPlan", back_populates = "meals")
    ing = relationship("Ingredients" , back_populates = "meal" , cascade = "all, delete-orphan")


class Ingredients(Base):
    __tablename__ = "ingredients"
    ing_id = Column(Integer , primary_key = True)
    meal_id = Column(Integer, ForeignKey("meal.meal_id"))
    name = Column(String , nullable = False)
    meal = relationship("Meal" , back_populates = "ing")
