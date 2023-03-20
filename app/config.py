from pydantic import BaseSettings


class Settings(BaseSettings):
    bot_token: str
    backend_host: str
    redis_host: str

    class Config:
        env_file = ".env"


settings = Settings()
