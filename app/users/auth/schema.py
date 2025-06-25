from pydantic import BaseModel, Field


class UserLoginSchema(BaseModel):
    user_id: int
    access_token: str
    # refresh_token: str


class GoogleUserData(BaseModel):
    id: int
    email: str
    verified_email: bool
    name: str
    access_token: str


class YandexUserData(BaseModel):
    id: int
    login: str
    name: str = Field(alias='real_name')
    email: str = Field(alias='default_email')
    access_token: str
