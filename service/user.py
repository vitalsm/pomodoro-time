from dataclasses import dataclass

from repository import UserRepository
from schemas import UserLoginSchema
from service.auth import AuthService


@dataclass
class UserService:
    user_repository: UserRepository
    auth_service: AuthService

    async def create_user(self, username: str, password: str) -> UserLoginSchema:
        hashed_pass = self.auth_service.get_hashed_password(password)
        user = await self.user_repository.create_user(username=username, password=hashed_pass)
        access_token = self.auth_service.generate_access_token(user_id=user.id)
        refresh_token = self.auth_service.generate_refresh_token(username)
        return UserLoginSchema(user_id=user.id, access_token=access_token, refresh_token=refresh_token)
