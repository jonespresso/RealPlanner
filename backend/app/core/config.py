from pydantic import BaseSettings
from dotenv import load_dotenv
import os

load_dotenv()  # Load variables from .env file into environment

class Settings(BaseSettings):
    PROJECT_NAME: str = "Realtor Planning App"
    API_V1_STR: str = "/api/v1"
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    GOOGLE_MAPS_API_KEY: str = os.getenv("GOOGLE_MAPS_API_KEY")

settings = Settings()