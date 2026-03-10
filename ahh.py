from enum import auto
import bcrypt
from fastapi import FastAPI, HTTPException,Response,status,Depends
from fastapi.params import Body
from httpx import post
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional,List
from random import randrange
from database import engine,sessionLocal,get_db
from sqlalchemy.orm import Session
import psycopg2
from psycopg2.extras import RealDictCursor
import time
import schemas
import models
import utils
from routers import posts,users,auth, vote
from config import settings

#while True:
#    try:
#        conn = psycopg2.connect(
#            host='localhost', 
#            database='fastapi', 
#            user='postgres', 
#            password='postgres',  
#            cursor_factory=RealDictCursor
#        )
#        cursor = conn.cursor()
#        print("Database connection was successful!")
#        break
#    except Exception as error:
#        print("Connecting to database failed")
#        print("Error: ", error)
#        time.sleep(2)

#models.Base.metadata.create_all(bind=engine)
app= FastAPI()
origins=['*']
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
   
app.include_router(posts.router)        
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(vote.router)             
@app.get("/")
def props():
    return {"message":"lets gooo!!!"}





