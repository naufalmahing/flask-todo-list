from __future__ import annotations 
from flask_sqlalchemy import SQLAlchemy
from typing import List, Optional

from sqlalchemy.orm import  (
    DeclarativeBase, 
    Mapped, 
    mapped_column, 
    relationship,
)
from sqlalchemy import (
    String,
    Table,
    Column,
    ForeignKey,
)

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

user_task_m2m = Table(
    'user_task',
    Base.metadata,
    Column('user_id', ForeignKey('user_table.id'), primary_key=True),
    Column('task_id', ForeignKey('task_table.id'), primary_key=True)
)

class User(Base):
    __tablename__ = 'user_table'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)

    tasks: Mapped[List[Task]] = relationship(
        secondary=user_task_m2m, back_populates='users'
    )

class Task(Base):
    __tablename__ = 'task_table'
    id: Mapped[int] = mapped_column(primary_key=True)
    task: Mapped[str] = mapped_column(String(100), nullable=False)
    done: Mapped[bool] = mapped_column(default=False)

    users: Mapped[List[User]] = relationship(
        secondary=user_task_m2m, back_populates='tasks'
    )

    # taskgroup_id: Mapped[int] = mapped_column(ForeignKey('taskgroup_table.id'))
    # taskgroups: Mapped['TaskGroup'] = relationship(back_populates='tasks')

class TaskGroup(Base):
    __tablename__ = 'taskgroup_table'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30), nullable=False, unique=True)

    # tasks: Mapped[List['Task']] = relationship(back_populates='taskgroups')