from contextlib import asynccontextmanager
from datetime import datetime
import aiohttp

ACCESS_TOKEN_LIFETIME = 1800  # 30 minutos (em segundos)
REFRESH_TOKEN_LIFETIME = 86400  # 24 horas (em segundos)


class TokenManager:

    def __init__(self, auth_endpoint, credentials):

        self.authentication_endpoint = auth_endpoint
        self.credentials = credentials

        self.access_token = None
        self.access_token_expiration = None

        self.refresh_token = None
        self.refresh_token_expiration = None

    @asynccontextmanager
    async def _session_context(self):
        async with aiohttp.ClientSession() as session:
            yield session

    def _access_token_expired(self):
        return (
            not self.access_token_expiration
            or datetime.now().timestamp() > self.access_token_expiration
        )

    def _refresh_token_expired(self):
        return (
            not self.refresh_token_expiration
            or datetime.now().timestamp() > self.refresh_token_expiration
        )

    def _update_tokens(self, tokens):
        self.access_token = tokens.get("access", None)
        self.refresh_token = tokens.get("refresh", None)
        self.access_token_expiration = (
            datetime.now().timestamp() + ACCESS_TOKEN_LIFETIME
        )
        self.refresh_token_expiration = (
            datetime.now().timestamp() + REFRESH_TOKEN_LIFETIME
        )

    async def _login(self):
        async with self._session_context() as session:
            async with session.post(
                self.authentication_endpoint,
                json=self.credentials,
            ) as response:
                tokens = await response.json()
                self._update_tokens(tokens)
                return self.access_token

    async def _refresh_access_token(self) -> None:
        body = {
            "refresh": self.refresh_token,
        }
        async with self._session_context() as session:
            async with session.post(
                self.authentication_endpoint + "refresh/",
                json=body,
            ) as response:
                tokens = await response.json()
                self._update_tokens(tokens)

    async def _refresh_or_login(self):
        if self._refresh_token_expired():
            await self._login()
        else:
            await self._refresh_access_token()

    async def get_access_token(self):
        if self._access_token_expired():
            await self._refresh_or_login()
        return self.access_token
