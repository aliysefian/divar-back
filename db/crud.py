from asyncio.log import logger
from select import select
from sqlite3 import IntegrityError
from pandas import array
from sqlalchemy.orm import Session

from . import models, schemas


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def get_posts(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Posts).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"

    db_user = models.User(
        email=user.email, hashed_password=fake_hashed_password)

    db.bulk_save_objects(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def create_posts(db: Session, posts):
    db_user = []
    cnt = 0
    for post in posts:

        image = post.get("web_images")
        if len(image) > 0:
            image = image[0][1]['src']
        else:
            image = None
        db_user = (
            models.Posts(price=post.get("price"),
                         web_images=image,
                         description=post.get("description"),
                         business_type=post.get("business_type"),
                         city=post.get("city"), 
                         brand_model=post.get("brand_model"),
                         token=post.get("token"),
                         title=post.get("title"), category=post.get("category"),
                         district=post.get("district"), url=post.get("url")
                         ))
        ex = db.query(models.Posts).filter(
            models.Posts.token == post.get("token")).first()

        if not ex:
            cnt = cnt+1
            db.add(db_user)
            db.commit()
    return cnt


def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Item).offset(skip).limit(limit).all()


def create_user_item(db: Session, item: schemas.ItemCreate, user_id: int):
    db_item = models.Item(**item.dict(), owner_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item
