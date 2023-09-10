
from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .. import database, schemas, models, utils, oauth2

router = APIRouter(tags = ["Authentication"])


@router.post("/login")
def login(userCredentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):

    #{
    #   username = *
    #   password = *
    #}
    
    user = db.query(models.User).filter(models.User.email == userCredentials.username).first()
    if not user:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail = f"Invalid Credentials")
    
    if not utils.verifyPassword(userCredentials.password, user.password):
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail = f"Invalid Credentials")
    
    # create a token
    accessToken = oauth2.createAccessToken(data = {"userId": user.id})

    # return token
    return {"access_token": accessToken, "token_type": "bearer"}