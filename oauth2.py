from imaplib import _Authenticator
from fastapi import Depends,status,HTTPException
from fastapi.security import OAuth2,OAuth2PasswordBearer
from jose import JWTError,jwt
from datetime import datetime,timedelta
from sqlalchemy.orm import Session
from config import settings
import database
import schemas
import models
OAuth2_scheme=OAuth2PasswordBearer(tokenUrl="login")
SECRET_KEY=settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

def create_access_token(data:dict):
    encode =data.copy()
    expire=datetime.utcnow()+timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    encode.update({"exp":expire})
    encoded_jwt=jwt.encode(encode,SECRET_KEY,algorithm=ALGORITHM)
    return encoded_jwt

def verify_acess_token(token:str,creditinals_execptions):
    try:
        payload=jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        id: str = str(payload.get("user_id")) 
        if id is None:
            raise creditinals_execptions
        token_data=schemas.TokenData(id=id)
    except JWTError:
        raise creditinals_execptions   
    return token_data 
    
def get_current_user(token:str=Depends(OAuth2_scheme),db: Session= Depends(database.get_db)):
    creditinals_execptions=HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                         detail="could not validate creditinals",
                                         headers={"WWW-Authenticate":"Bearer"})
    token=verify_acess_token(token,creditinals_execptions)
    user=db.query(models.User).filter(models.User.id==token.id).first()
    return user



