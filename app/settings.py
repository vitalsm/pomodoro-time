import os
import ssl

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    BASE_DIR: str = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    DB_LOGIN: str
    DB_PASS: str
    DB_SERVER: str
    DB_PORT: int
    DB_NAME: str
    DB_DRIVER: str
    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_DB: int
    REDIS_PASSWORD: str
    REDIS_USER: str
    REDIS_USER_PASSWORD: str
    JWT_SECRET_KEY: str
    JWT_REFRESH_SECRET_KEY: str
    JWT_ENCODE_ALGORITHM: str
    ACCESS_TOKEN_LIFETIME_MINUTES: int
    REFRESH_TOKEN_LIFETIME_MINUTES: int
    GOOGLE_CLIENT_ID: str
    GOOGLE_CLIENT_SECRET: str
    GOOGLE_REDIRECT_URI: str
    GOOGLE_TOKEN_URI: str
    YANDEX_CLIENT_ID: str
    YANDEX_CLIENT_SECRET: str
    YANDEX_REDIRECT_URI: str
    YANDEX_TOKEN_URI: str
    FROM_EMAIL: str
    SMTP_PORT: int
    SMTP_HOST: str
    SMTP_PASSWORD: str
    RABBITMQ_USER: str
    RABBITMQ_PASS: str
    RABBITMQ_PORT: int
    TEST_GOOGLE_EMAIL: str
    BROKER_URL: str = 'localhost:9092'
    EMAIL_TOPIC: str = 'email_topic'
    EMAIL_CALLBACK_TOPIC: str = 'email_callback_topic'


    @property
    def celery_broker_url(self) -> str:
        return f'amqp://{self.RABBITMQ_USER}:{self.RABBITMQ_PASS}@localhost:{self.RABBITMQ_PORT}//'

    @property
    def database_url(self) -> str:
        return f"{self.DB_DRIVER}://{self.DB_LOGIN}:{self.DB_PASS}@{self.DB_SERVER}:{self.DB_PORT}/{self.DB_NAME}"

    @property
    def google_redirect_url(self) -> str:
        return f"https://accounts.google.com/o/oauth2/auth?response_type=code&client_id={self.GOOGLE_CLIENT_ID}&redirect_uri={self.GOOGLE_REDIRECT_URI}&scope=openid%20profile%20email&access_type=offline"

    @property
    def yandex_redirect_url(self) -> str:
        return f"https://oauth.yandex.ru/authorize?response_type=code&client_id={self.YANDEX_CLIENT_ID}&force_confirm=yes"

    model_config = SettingsConfigDict(env_file=f"{BASE_DIR}/.local.env")


# Опции для работы с SSL, отключаем проверку сертификата (подходит для отладки)
ssl_options = {"ssl_cert_reqs": ssl.CERT_NONE}

settings = Settings()
