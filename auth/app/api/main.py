from sqlite3 import IntegrityError
from typing import Optional
from fastapi import Depends, FastAPI, HTTPException, Request, Response
from fastapi.responses import RedirectResponse
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from app.api.schemas.user import (
    UserRead,
    UserCreate
)
from app.db.db import get_session
from app.db.repositories.user_repository.user_repo import UserRepository
from app.settings import settings
from .routers import api_router
from sqlalchemy.exc import IntegrityError
from .authorization.func import get_current_user
from app.db.repositories.role_repo.role_repo import RoleRepository
from google_auth_oauthlib import flow
from authlib.integrations.starlette_client import OAuth
from google.oauth2 import id_token
from google.auth.transport import requests


app = FastAPI(
    title=settings.PROJECT_TITLE, 
    version="1.0.0",
    root_path=settings.FAST_API_PREFIX
    )

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.exception_handler(IntegrityError)
async def integrity_error_handler(exc: IntegrityError):
    raise HTTPException(status_code=400, detail=str(exc.orig).split("\nDETAIL:  ")[1])


app.include_router(api_router)

@app.get("/GET", response_model=UserRead)
async def get(user: UserRead = Depends(get_current_user)):
    if user.role != "admin":
        raise HTTPException(status_code=403, detail="Acces denied")
    return user

@app.get("/authorize")
async def authorize_google_oauth2() -> Response:
    auth_flow = flow.Flow.from_client_secrets_file(
        client_secrets_file=f'{settings.DIRECTORY}/certs/credentials.json',
        scopes=_get_scopes(),
    )
    auth_flow.redirect_uri = "https://bytecode.su/auth/api/oauth2callback"

    authorization_url, _ = auth_flow.authorization_url(
        access_type="offline",
        include_granted_scopes="true",
        login_hint='hint@example.com',
        prompt='consent'
    )

    return RedirectResponse(url=authorization_url)


def _get_scopes() -> list[str]:
    return [
        "openid",
        "https://www.googleapis.com/auth/userinfo.profile",
        "https://www.googleapis.com/auth/userinfo.email",
    ]


@app.get("/oauth2callback")
async def oauth2callback_google_oauth2(
    request: Request,
    state: str | None = None,
) -> Response:
    auth_flow = flow.Flow.from_client_secrets_file(
        client_secrets_file=f'{settings.DIRECTORY}/certs/credentials.json',
        scopes=_get_scopes(),
        state=state,
    )
    auth_flow.redirect_uri = "https://bytecode.su/auth/api/oauth2callback"

    authorization_response = str(request.url)
    print(authorization_response)
    auth_flow.fetch_token(authorization_response=authorization_response)

    credentials = auth_flow.credentials
    print(credentials.token_state)
    with open("oauth_credentials.json", "w") as fout:
        fout.write(credentials.to_json())

    return RedirectResponse(url="https://www.google.com")