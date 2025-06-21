from dataclasses import dataclass

import httpx
from fastapi import HTTPException

from schemas import YandexUserData
from settings import settings


@dataclass
class YandexClient:
    settings: settings
    async_client: httpx.AsyncClient

    async def get_user_info(self, code: str) -> YandexUserData:
        access_token = self._get_user_access_token(code=code)
        async with self.async_client as client:
            user_info = await client.get(
                'https://login.yandex.ru/info?format=json',
                headers={'Authorization': f'OAuth {access_token}'}
            )
        return YandexUserData(**user_info.json(), access_token=access_token)

    async def _get_user_access_token(self, code: str) -> str:
        async with self.async_client as client:
            response = await client.post(
                self.settings.YANDEX_TOKEN_URI,
                data = {
                    'code': code,
                    'client_id': self.settings.YANDEX_CLIENT_ID,
                    'client_secret': self.settings.YANDEX_CLIENT_SECRET,
                    'grant_type': 'authorization_code'
                },
                headers = {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
            )

            if response.status_code == 200:
                return response.json()['access_token']
            else:
                raise HTTPException(
                    status_code=response.status_code,
                    detail=response.json()['error_description']
                )
