from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, func,DateTime
from sqlalchemy.orm import relationship

from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

    items = relationship("Item", back_populates="owner")


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="items")


class Posts(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    business_type = Column(String, index=True,nullable=True)
    price = Column(String, index=True,nullable=True)
    brand_model = Column(String, index=True,nullable=True)
    city = Column(String, index=True,nullable=True)
    token = Column(String, index=True,nullable=True,unique=True)
    Local_modified = Column(DateTime, server_default=func.now(), onupdate=func.now())

    list_data = Column(String, index=True,nullable=True)
    web_images = Column(String, index=True,nullable=True)
    description = Column(String, index=True,nullable=True)
#   "description":data.get("description"), 
#         "business_type":data.get("business_data")["business_type"],
#         "price":data.get("webengage")["price"],
#         "brand_model":data.get("webengage")["brand_model"],
#         "city":data.get("webengage")["city"],
#         "token":data.get("webengage")["token"],
#         "title":widgets.get("header")["title"],
#           "date":widgets.get("header")["date"],
#         "list_data":widgets.get("list_data"),
#         "web_images":widgets.get("web_images"), 