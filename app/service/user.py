from dataclasses import dataclass

from app.repository import UserRepository
from app.schemas import UserLoginSchema, UserCreateSchema
from app.service.auth import AuthService


@dataclass
class UserService:
    user_repository: UserRepository
    auth_service: AuthService

    async def create_user(self, user: UserCreateSchema) -> UserLoginSchema:
        hashed_pass = self.auth_service.get_hashed_password(user.password)
        user.password = hashed_pass
        user = await self.user_repository.create_user(user)
        access_token = self.auth_service.generate_access_token(user_id=user.id)
        refresh_token = self.auth_service.generate_refresh_token(user.username)
        return UserLoginSchema(user_id=user.id, access_token=access_token)
