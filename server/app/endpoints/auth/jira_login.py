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


@router.get('/jiralogin')
def github_login():
    """_summary_

    Returns:
        _type_: _description_
    """
    return RedirectResponse(f"""https://auth.atlassian.com/authorize?
                            audience=api.atlassian.com&
                            client_id={os.getenv("JIRA_CLIENT_ID")}&
                            scope=REQUESTED_SCOPE_ONE%20REQUESTED_SCOPE_TWO&
                            redirect_uri={os.getenv("FRONTEND_URL")}&
                            state=YOUR_USER_BOUND_VALUE&
                            response_type=code&
                            prompt=consent""")



@router.get('/githublogin/redirect')
def github_redirect(code:str, user_id:str):
    """_summary_

    Args:
        code (str): _description_
    """
    header = {
        "Accept": "application/json"
    }
    
    body_args = {
        "client_id" : os.getenv("JIRA_CLIENT_ID"),
        "client_secret": os.getenv("JIRA_CLIENT_SECRET"),
        "code": code,
        "redirect_url":os.getenv("FRONTEND_URL")

    }

    response = requests.post("https://auth.atlassian.com/oauth/token",headers=header,data = body_args, timeout=20)

    
    if response.status_code == 200:
        print(f"{response.json()=}")
        datasource = None
        datasource = session.query(DataSource).filter_by(type='jira').first()
        if datasource is None:
            datasource = DataSource(id = str(uuid.uuid4()), name="Jira", type = "jira")
            session.add(datasource)
            session.commit()
        
        userdatasource = UserDataSource(user_id = user_id,data_source_id = datasource.id, credentials = encrypt_data(response.json().get("access_token")))
        session.add(userdatasource)
        session.commit()
        return JSONResponse(status_code = response.status_code, content="got the access token")
    else:
        return JSONResponse(status_code = requests.status_codes, content = response.json())

    

    
@router.get('/checkjiratoken')
def github_token(user_id:str):
    """_summary_

    Args:
        user_id (str): _description_

    Returns:
        _type_: _description_
    """
    token_data = session.query(UserDataSource).filter_by(user_id = user_id).first()

    if token_data is None:
        return JSONResponse(status_code=200, content = False)
    return JSONResponse(status_code=200,content=True)

