from dataclasses import dataclass
from datetime import datetime as dt, timedelta, timezone
from typing import Union, Any

from passlib.context import CryptContext

from jose import jwt, JWTError

from app.exception import UserNotFoundExeption, UserPasswordException, TokenNotCorrect, TokenExpired
from app.models import UserProfile
from app.repository import UserRepository
from app.schemas import UserLoginSchema, UserCreateSchema, GoogleUserData, YandexUserData
from app.settings import settings
from app.clients import GoogleClient, YandexClient


@dataclass
class AuthService:
    user_repository: UserRepository
    settings: settings
    google_client: GoogleClient
    yandex_client: YandexClient

    password_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

    def get_hashed_password(self, password: str) -> str:
        return self.password_context.hash(password)

    def verify_password(self, password: str, hashed_pass: str) -> bool:
        return self.password_context.verify(password, hashed_pass)

    async def google_auth(self, code: str):
        user_data = await self.google_client.get_user_info(code)
        return await self.oauth_login(user_data)

    async def yandex_auth(self, code: str):
        user_data = await self.yandex_client.get_user_info(code=code)
        return await self.oauth_login(user_data)

    async def oauth_login(self, user_data: GoogleUserData | YandexUserData) -> UserLoginSchema:
        if user := await self.user_repository.get_user_by_email(email=user_data.email):
            access_token = self.generate_access_token(user_id=user.id)
            return UserLoginSchema(user_id=user.id, access_token=access_token)

        create_user_data = UserCreateSchema(
            email=user_data.email,
            name=user_data.name,
        )
        created_user = await self.user_repository.create_user(create_user_data)
        access_token = self.generate_access_token(user_id=created_user.id)
        return UserLoginSchema(user_id=created_user.id, access_token=access_token)

    def get_google_redirect_url(self) -> str:
        return self.settings.google_redirect_url

    def get_yandex_redirect_url(self) -> str:
        return self.settings.yandex_redirect_url

    async def login(self, username: str, password: str) -> UserLoginSchema:
        user = await self.user_repository.get_user_by_username(username)
        self._validate_auth_user(user, password)
        access_token = self.generate_access_token(user_id=user.id)
        return UserLoginSchema(user_id=user.id, access_token=access_token)

    def _validate_auth_user(self, user: UserProfile, password: str):
        if not user:
            raise UserNotFoundExeption
        if not self.verify_password(password=password, hashed_pass=user.password):
            raise UserPasswordException

    def generate_access_token(self, user_id: int) -> str:
        expire_date_unix = (dt.now(timezone.utc) + timedelta(minutes=self.settings.ACCESS_TOKEN_LIFETIME_MINUTES)).timestamp()
        payload = {'user_id': user_id, 'exp': expire_date_unix}
        token = jwt.encode(payload, self.settings.JWT_SECRET_KEY, algorithm=self.settings.JWT_ENCODE_ALGORITHM)
        return token

    def generate_refresh_token(self, subject: Union[str, Any]) -> str:
        expire_date_unix = (dt.now(timezone.utc) + timedelta(minutes=self.settings.REFRESH_TOKEN_LIFETIME_MINUTES)).timestamp()
        payload = {'sub': str(subject), 'exp': expire_date_unix}
        token = jwt.encode(payload, self.settings.JWT_REFRESH_SECRET_KEY, algorithm=self.settings.JWT_ENCODE_ALGORITHM)
        return token

    def get_user_id_from_access_token(self, access_token: str) -> int:
        try:
            payload = jwt.decode(
                access_token,
                self.settings.JWT_SECRET_KEY,
                algorithms=[self.settings.JWT_ENCODE_ALGORITHM])
        except JWTError:
            raise TokenNotCorrect

        if payload['exp'] < dt.now(timezone.utc).timestamp():
            raise TokenExpired

        return payload['user_id']
