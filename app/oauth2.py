# documentation: https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/#handle-jwt-tokens

from datetime import datetime, timedelta
from jose import JWTError, jwt
from app.schemas import Token
from . import schemas, database, models
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl = 'login')



# secret_key verifies the integrity of our token
# algorithm
# expiration time of the token (how long the user can stay logged in)

# to get a string like this run:
# openssl rand -hex 32

SECRET_KEY = settings.secret_key  # WE CANNOT HAVE THIS EXPOSED HERE --> Set it as env variable
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes


def create_access_token(data: dict):
    to_encode = data.copy()   # data to encode in our token
    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


# Verify access token
def verify_access_token(token: str, credentials_exception):

    try:
        payload =  jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])  # decode token using SECRET_KEY and ALGORITHM
        id = payload.get("user_id")  # extract id

        if id is None:
            raise credentials_exception
        token_data = schemas.TokenData(id=str(id))  # we only have id to extract

    except JWTError:
        raise credentials_exception

    return token_data
    
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    # Calling verify_access_token
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                                          detail=f"could not validate credentials", 
                                          headers={"WWW-Authenticate": "Bearer"})
    
    token = verify_access_token(token, credentials_exception)
    user = db.query(models.User).filter(models.User.id == token.id).first()
    return user