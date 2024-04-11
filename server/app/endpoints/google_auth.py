# pylint: disable=import-error
import os

import jwt
import requests  # Add this import for HTTP requests
from app.db.database import session
from app.models.user import Role, User
from dotenv import load_dotenv
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError

load_dotenv()

router = APIRouter()

# OAuth settings
GOOGLE_CLIENT_ID = os.getenv('CLIENT_ID') or None
GOOGLE_CLIENT_SECRET = os.getenv('CLIENT_SECRET') or None
GOOGLE_REDIRECT_URI = os.getenv("FRONTEND_URL")


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")  # Assuming you have a token endpoint


async def get_current_user(token: str = Depends(oauth2_scheme)):
    """_summary_

    Args:
        token (str, optional): _description_. Defaults to Depends(oauth2_scheme).
        db (Session, optional): _description_. Defaults to Depends(get_db).

    Raises:
        credentials_exception: _description_
        credentials_exception: _description_
        credentials_exception: _description_
        credentials_exception: _description_

    Returns:
        _type_: _description_
    """
    credentials_exception = HTTPException(
        status_code=401, detail="Could not validate credentials"
    )
    try:
        payload = jwt.decode(token, jwt_secret_key, algorithms=[jwt_algorithm])
        google_token = payload.get("google_token")
        if google_token is None or not await verify_google_token(google_token):
            raise credentials_exception
        user_id = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        user = session.query(User).filter_by(id = user_id).first()
        if user is None:
            raise credentials_exception
    except JWTError as exc:
        raise credentials_exception from exc
    return user

@router.get('/login')
async def login():
    """_summary_

    Args:
        request (Request): _description_

    Returns:
        _type_: _description_
    """
    return RedirectResponse(f"https://accounts.google.com/o/oauth2/auth?response_type=code&client_id={GOOGLE_CLIENT_ID}&redirect_uri={GOOGLE_REDIRECT_URI}&scope=openid%20profile%20email&access_type=offline")

@router.get('/auth')
async def auth(code : str):
    """_summary_

    Args:
        request (Request): _description_
        db (Session, optional): _description_. Defaults to Depends(get_db).

    Raises:
        HTTPException: _description_

    Returns:
        _type_: _description_
    """
    token_url = "https://accounts.google.com/o/oauth2/token"
    data = {
        "code": code,
        "client_id": GOOGLE_CLIENT_ID,
        "client_secret": GOOGLE_CLIENT_SECRET,
        "redirect_uri": GOOGLE_REDIRECT_URI,
        "grant_type": "authorization_code",
    }
    response = requests.post(token_url, data=data, timeout=10)
    access_token = response.json().get("access_token")
    response = requests.get("https://www.googleapis.com/oauth2/v1/userinfo", headers={"Authorization": f"Bearer {access_token}"}, timeout=10)
    user_info = response.json()
    print(f"{user_info=}")
    if user_info:
        roles = session.query(Role).all()

        if not roles:
            role = Role(id='2', role_name= 'user')
            session.add(role)
            session.commit()
            session.refresh(role)
        user = session.query(User).filter_by(email = user_info['email']).first()
        if not user:
            user = User(
                email=user_info['email'],
                name=user_info['name'],
                role_id = '2'
            )
            session.add(user)
            session.commit()
            session.refresh(user)

        return JSONResponse(status_code=200, content= {
            "id":user.id,
            "name": user.name,
            "email": user.email
        })
    else:
        raise HTTPException(status_code=400, detail="User information not found.")

# Example of a protected route
@router.get("/token")
async def protected_route(current_user: User = Depends(get_current_user)):
    """_summary_

    Args:
        current_user (User, optional): _description_. Defaults to Depends(get_current_user).

    Returns:
        _type_: _description_
    """
    return current_user

# Add other endpoints as needed
