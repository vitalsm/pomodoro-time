from dataclasses import dataclass

import httpx
from fastapi import HTTPException

from schemas import GoogleUserData
from settings import settings


@dataclass
class GoogleClient:
    settings: settings
    async_client: httpx.AsyncClient

    async def get_user_info(self, code: str) -> GoogleUserData:
        access_token = self._get_user_access_token(code=code)
        async with self.async_client as client:
            user_info = await client.get(
                'https://www.googleapis.com/oauth2/v1/userinfo',
                headers={'Authorization': f'Bearer {access_token}'}
            )
        return GoogleUserData(**user_info.json(), access_token=access_token)

    async def _get_user_access_token(self, code: str) -> str:
        data = {
            'code': code,
            'client_id': self.settings.GOOGLE_CLIENT_ID,
            'client_secret': self.settings.GOOGLE_CLIENT_SECRET,
            'redirect_uri': self.settings.GOOGLE_REDIRECT_URI,
            'grant_type': 'authorization_code'
        }
        async with self.async_client as client:
            response = await client.post(self.settings.GOOGLE_TOKEN_URI, data=data)

            if response.status_code == 200:
                return response.json()['access_token']
            else:
                raise HTTPException(
                    status_code=response.status_code,
                    detail=response.json()['error_description']
                )
