from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session
from app.api import deps

from app import models, schemas, crud

router = APIRouter()


@router.get("")
async def default():
    return {"message": "Hello World"}


@router.get("/feeds/", response_model=list[schemas.Feed])
def get_feeds(skip: int = 0, limit: int = 100, db: Session = Depends(deps.get_db)):
    # Retrieve all users from the database with pagination parameters
    feeds = crud.feeds.get_feeds(db, skip=skip, limit=limit)
    return feeds
