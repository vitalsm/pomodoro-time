from dataclasses import dataclass

import httpx
from fastapi import HTTPException

from app.schemas import YandexUserData
from app.settings import settings


@dataclass
class YandexClient:
    settings: settings
    async_client: httpx.AsyncClient

    async def get_user_info(self, code: str) -> YandexUserData:
        access_token = await self._get_user_access_token(code=code)
        user_info = await self.async_client.get(
            'https://login.yandex.ru/info?format=json',
            headers={'Authorization': f'OAuth {access_token}'}
        )
        await self.async_client.aclose()

        return YandexUserData(**user_info.json(), access_token=access_token)

    async def _get_user_access_token(self, code: str) -> str:
        response = await self.async_client.post(
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
