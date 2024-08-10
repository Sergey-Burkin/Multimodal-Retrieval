from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from src.models.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    # email = Column(String, index=True)
    hashed_password = Column(String(length=1024))
    # disabled = Column(Boolean, default=False)

    username = Column(String, unique=True, nullable=True)
    # full_name = Column(String, nullable=True)

    items = relationship("Item", back_populates="owner")


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="items")
