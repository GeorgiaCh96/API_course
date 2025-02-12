from pydantic_settings import BaseSettings
#from app.oauth2 import ALGORITHM

class Settings(BaseSettings):
    # PROVIDE THE LIST OF ENVIRONMENT VARIABLES YOU WANT TO SET
    database_hostname: str
    database_port: int
    database_password: str
    database_name: str
    database_username: str
    secret_key: str
    algorithm: str  = "HS256" 
    access_token_expire_minutes: int

    class Config:
        env_file = ".env"


settings = Settings()
print(settings.database_password)