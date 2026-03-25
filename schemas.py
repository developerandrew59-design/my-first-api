from typing import Optional
from pydantic import BaseModel,EmailStr
from datetime import datetime
from pydantic.types import conint

from typing import Literal
class PostBase(BaseModel):
    title:str
    content:str
    published: bool=True
    
    
class PostCreate(PostBase):
    pass

class UserOut(BaseModel):
    email:EmailStr
    id:int
    created_at:datetime 
    
    class config():
        orm_mode=True

class Post(PostBase):
    id:int
    created_at:datetime
    account_id:int
    details:UserOut
    class config():
        orm_mode=True

class Postout(BaseModel):
    Post:Post
    votes:int
    class config():
        orm_mode=True


class UserCreate(BaseModel):
    email:EmailStr
    password:str 
    


        
class UserLogin(BaseModel):
    email:EmailStr
    password:str    

class Token(BaseModel):
    acess_token: str
    token_type: str

class TokenData(BaseModel):
    id:Optional[str]=None


class Vote(BaseModel):
    post_id:int
    dir:Literal[0, 1]