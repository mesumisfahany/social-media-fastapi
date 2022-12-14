from pydantic import BaseSettings


class Settings(BaseSettings):
    # Only for validation
    database_hostname: str
    database_port: str
    database_password: str
    database_name: str
    database_username: str

    secret_key: str
    algorithim: str
    access_token_expire_minutes: int

    class Config:
        env_file = ".env"


settings = Settings()