import base64
import os
import uuid

import requests
from app.db.database import session
from app.models.datasource import DataSource, UserDataSource
from app.utils.secure_token import encrypt_data
from dotenv import load_dotenv
from fastapi import APIRouter
from fastapi.responses import JSONResponse, RedirectResponse

load_dotenv()

router = APIRouter()


@router.get('/slacklogin')
def slack_login():
    """_summary_

    Returns:
        _type_: _description_
    """
    return RedirectResponse(f"https://slack.com/oauth/v2/authorize?scope=channels:read,channels:history,groups:history,groups:read,im:history,im:read,mpim:history,mpim:read,users:read&client_id={os.getenv('SLACK_CLIENT_ID')}")



@router.get('/slacklogin/redirect')
def slack_redirect(code:str, user_id:str):
    """_summary_

    Args:
        code (str): _description_
    """
    
    body_args = {
        "client_id" : os.getenv("SLACK_CLIENT_ID"),
        "client_secret": os.getenv("SLACK_CLIENT_SECRET"),
        "code": code,
        "redirect_url":os.getenv("FRONTEND_URL")

    }
    header = {
        "Accept": "application/json"
    }

    response = requests.post("https://slack.com/api/oauth.v2.access",headers=header,data = body_args, timeout=20)

    
    if response.status_code == 200:
        datasource = None
        datasource = session.query(DataSource).filter_by(type='slack').first()
        if datasource is None:
            datasource = DataSource(id = str(uuid.uuid4()), name="Slack", type = "slack")
            session.add(datasource)
            session.commit()
        
        encrypted_token,_= base64.b64encode(encrypt_data(response.json().get("access_token"))).decode('utf-8'),response.json().get("access_token")
        userdatasource = UserDataSource(user_id = user_id,data_source_id = datasource.id, credentials = encrypted_token)
        session.add(userdatasource)
        session.commit()
        return JSONResponse(status_code = response.status_code, content="got the access token")
    else:
        return JSONResponse(status_code = requests.status_codes, content = response.json())

    

    
@router.get('/checkslacktoken')
def github_token(user_id:str, source_type :str):
    """_summary_

    Args:
        user_id (str): _description_

    Returns:
        _type_: _description_
    """
    token_data = session.query(UserDataSource).join(DataSource).filter(DataSource.type == source_type,UserDataSource.user_id == user_id).first()

    if token_data is None:
        return JSONResponse(status_code=200, content = False)
    return JSONResponse(status_code=200,content=True)