from pathlib import Path
from pydantic_settings import BaseSettings

minutesinaday=60*24
BASE_DIR = Path(__file__).resolve().parent.parent.parent  

class Settings(BaseSettings):

    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str

    GOOGLE_CLIENT_ID: str
    ALLOWED_EMAIL_DOMAINS: str = "unal.edu.co"
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_MINUTES: int = minutesinaday

    class Config:
        env_file = BASE_DIR / ".env"

    @property
    def allowed_domains_list(self) -> list[str]:
        return [d.strip().lower() for d in self.ALLOWED_EMAIL_DOMAINS.split(",") if d.strip()]

settings = Settings()