from sqlalchemy import Column , Integer , String , DateTime , Identity , ForeignKey, Table, JSON
from sqlalchemy.orm import relationship
from Data_Layer.DB_Context import Base


board_users = Table(
    "board_users",
    Base.metadata,
    Column("board_id", ForeignKey("boards.id"), primary_key=True),
    Column("user_id", ForeignKey("users.id"), primary_key=True),
)

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, Identity(start=1, increment=1), primary_key=True)
    name = Column(String, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    creation_date = Column(DateTime)

    boards = relationship("Board",secondary=board_users,back_populates="users") # many-to-many relationship
    created_tasks = relationship("Task",foreign_keys="Task.created_by",back_populates="creator") #task creator
    updated_tasks = relationship("Task",foreign_keys="Task.updated_by",back_populates="updater") #task updater


class Board(Base):
    __tablename__ = "boards"

    id = Column(Integer, Identity(start=1, increment=1), primary_key=True)
    title = Column(String, index=True, nullable=False, unique=True)
    creation_date = Column(DateTime)
    created_by = Column(Integer, ForeignKey("users.id"))

    users = relationship("User",secondary=board_users,back_populates="boards") # many to many relationsship with users
    tasks = relationship("Task",back_populates="board",cascade="all, delete-orphan") # one-to-many relationship with tasks
    creator = relationship("User",foreign_keys=[created_by]) # one-to-many relationship with users as creators

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True)
    description = Column(String)
    created_at = Column(DateTime,index=True)
    updated_at = Column(DateTime)
    status = Column(String)  # Example: "open", "in_progress", "done"

    board_id = Column(Integer, ForeignKey("boards.id"))
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    updated_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    data = Column(JSON, default={})  # stores dynamic user-defined fields

    # Relationships
    board = relationship("Board", back_populates="tasks")
    creator = relationship("User", foreign_keys=[created_by], back_populates="created_tasks")
    updater = relationship("User", foreign_keys=[updated_by], back_populates="updated_tasks")
