from fastapi import FastAPI, HTTPException,Response,status,Depends,APIRouter
from pydantic import Tag
from sqlalchemy.orm import Session
from database import engine,sessionLocal,get_db
import models,schemas
from typing import List
from utils import hash
import oauth2
router=APIRouter(
    prefix="/users",
    tags=['Users']
    )
    

@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.UserOut)

def create_user(user: schemas.UserCreate,db: Session = Depends(get_db)):
    hashed_password=hash(user.password)
    user.password=hashed_password
    new_user=models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/{id}",response_model=schemas.UserOut)
def get_user(id:int,db: Session = Depends(get_db)):
    user= db.query(models.User).filter(models.User.id==id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"user with id {id} not found")
    return user

@router.get("/",response_model=List[schemas.UserOut])
def get_all_users(db: Session = Depends(get_db)):
    user=db.query(models.User).all()
    return user