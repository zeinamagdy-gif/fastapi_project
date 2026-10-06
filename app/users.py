import uuid
from typing import Optional
from fastapi import Depends, Request
from fastapi_users import BaseUserManager, UUIDIDMixin, models,FastAPIUsers
from fastapi_users.authentication import (
    AuthenticationBackend,
    BearerTransport,
    JWTStrategy
)
from fastapi_users.db import SQLAlchemyUserDatabase
from db import User, get_user_db
SECRET="JkZm_1997"


class UserManager(UUIDIDMixin,BaseUserManager[User,uuid.UUID]):
    reset_password_token_secret = SECRET
    verification_token_secret = SECRET

    async def on_after_register(
        self, user: User, request: Optional[Request]  = None):
        print(f"User{user.id}Has Registred")
    async def on_after_forgot_password(
        self, user: User, token: str, request:Optional[ Request] = None):
        print(f"User{user.id} Has Forgot Their Password")
    async def on_after_request_verify(self,user:User,token: str, request:Optional[ Request] = None):
        print(f"Verfy request from User {user.id}. Reset  Token: {token} ")
async def get_user_manger(user_db:SQLAlchemyUserDatabase=Depends(get_user_db)):
    yield UserManager(user_db)
bearer_transport=BearerTransport(tokenUrl="auth/jwt/login")
def get_jwt_strategy():
    return JWTStrategy(secret=SECRET,lifetime_seconds=3600)
auth_backend=AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,

)
fastapi_users= FastAPIUsers[User,uuid.UUID](get_user_manger,auth_backends=[auth_backend])
current_active_user=fastapi_users.current_user(active=True)

