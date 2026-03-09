from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_HOST: str
    DATABASE_PORT: int
    DATABASE_USER: str
    DATABASE_PASSWORD: str
    DATABASE_NAME: str

    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_HOURS: int
    ALGORITHM: str
    APP_NAME: str

    @property
    def DATABASE_URL(self):
        return (
            f"postgresql://{self.DATABASE_USER}:"
            f"{self.DATABASE_PASSWORD}@"
            f"{self.DATABASE_HOST}:"
            f"{self.DATABASE_PORT}/"
            f"{self.DATABASE_NAME}"
        )

    class Config:
        env_file = ".env"

settings = Settings()
DATABASE_URL =settings.DATABASE_URL
SECRET_KEY = settings.SECRET_KEY
ACCESS_TOKEN_EXPIRE_HOURS = settings.ACCESS_TOKEN_EXPIRE_HOURS
ALGORITHM = settings.ALGORITHM
APP_NAME=settings.APP_NAME