from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    API_TOKEN: str = "your-secret-token"
    REDIS_URL: str = "redis://localhost:6379"
    BASE_URL: str = "https://dentalstall.com/shop/"
    RETRY_ATTEMPTS: int = 3
    RETRY_WAIT_SECONDS: int = 5
    
    class Config:
        env_file = ".env"

settings = Settings()
