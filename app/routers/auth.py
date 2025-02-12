from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session
from .. import database, schemas, models, utils, oauth2
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

router = APIRouter(tags = ['Authentication'])

@router.post('/login', response_model=schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    
    """
        user_credentials will return username and password only (won't return email --> change user_Credentials.email below to user_credentials.username)

    {
        "username": "123",
        "password": "123"
    }
    
    !! Login through postman: instead of ussing Body > JSON raw format, use Body> form-data format
    """
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")
    
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")
    

    # CREATE TOKEN
    # return token

    access_token = oauth2.create_access_token(data = {"user_id": user.id})
    return {"access_token" : access_token, "token_type": "bearer"}