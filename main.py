from typing import List
import requests

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from db import crud, models, schemas
from db.database import SessionLocal, engine
from db.api import get_data_from_divar
from fastapi_utils.tasks import repeat_every
from fastapi.middleware.cors import CORSMiddleware
from fastapi_pagination import Page, add_pagination, paginate


origins = ["*"]



models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# @app.post("/users/", response_model=schemas.User)
# def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
#     db_user = crud.get_user_by_email(db, email=user.email)
#     if db_user:
#         raise HTTPException(status_code=400, detail="Email already registered")
#     return crud.create_user(db=db, user=user)


@app.get("/period-call/")
def read_users(city="isfahan", db: Session = Depends(get_db)):
    print(city)
    data=get_data_from_divar(city=city)
    posts= crud.create_posts(db,data)
    print("finised",posts)
    return {}

@app.on_event("startup")
@repeat_every(seconds=180) 
def call_back():
    print("start")
    response=requests.get('http://127.0.0.1:8000/period-call/?skip=0&limit=100')
    print("=fi",response.status_code)


@app.on_event("startup")
@repeat_every(seconds=200) 
def call_back_city():
    print("start")
    response=requests.get('http://127.0.0.1:8000/period-call/?city=tehran')
    print("=fi",response.status_code)
# @app.get("/users/{user_id}", response_model=schemas.User)
# def read_user(user_id: int, db: Session = Depends(get_db)):
#     db_user = crud.get_user(db, user_id=user_id)
#     if db_user is None:
#         raise HTTPException(status_code=404, detail="User not found")
#     return db_user


# @app.post("/users/{user_id}/items/", response_model=schemas.Item)
# def create_item_for_user(
#     user_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)
# ):
#     return crud.create_user_item(db=db, item=item, user_id=user_id)


# @app.get("/items/", response_model=List[schemas.Item])
# def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
#     items = crud.get_items(db, skip=skip, limit=limit)
#     return items

@app.get("/posts/",response_model=Page[schemas.Posts])
def read_posts(city="isfahan", db: Session = Depends(get_db)):
    items = paginate(crud.get_posts(db,city=city))
    return items
add_pagination(app)