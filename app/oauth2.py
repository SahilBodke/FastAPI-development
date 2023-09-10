from jose import JWTError, jwt
from datetime import datetime, timedelta
from . import schemas, database, models
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .config import settings

oauth2Scheme = OAuth2PasswordBearer(tokenUrl="login")

#SECRET_KEY
#Algorithm
#EXPIRATION_TIME 

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes


def createAccessToken(data: dict):

    toEncode = data.copy()
    expire = datetime.now() + timedelta(minutes = ACCESS_TOKEN_EXPIRE_MINUTES)  # 60 mins from now

    toEncode.update({"expiration": expire.strftime('%Y-%m-%dT%H:%M:%S')})

    # toEncode.update({"expiration": expire})

    encodedJwt = jwt.encode(toEncode, SECRET_KEY, algorithm = ALGORITHM)
    return encodedJwt


def verifyAccessToken(token: str, credentialsException):

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get("userId")
        id = str(id)
        if id is None:
            raise credentialsException
        tokenData = schemas.TokenData(id=id)
    
    except JWTError as e:
        raise credentialsException
    
    return tokenData
    
def getCurrentUser(token: str = Depends(oauth2Scheme), db: Session = Depends(database.get_db)):

    credentialsException = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail = f"Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})
    token = verifyAccessToken(token, credentialsException)
    
    user = db.query(models.User).filter(models.User.id == token.id).first()

    return user
