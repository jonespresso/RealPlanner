from pydantic_settings import BaseSettings
from dotenv import load_dotenv, find_dotenv
import os
import json
from pathlib import Path
from typing import Optional

# Robustly load .env from the nearest parent directory using find_dotenv
load_dotenv(find_dotenv())

class Settings(BaseSettings):
    PROJECT_NAME: str = "Realtor Planning App"
    API_V1_STR: str = "/api/v1"
    DATABASE_URL: Optional[str] = None
    GOOGLE_MAPS_API_KEY: Optional[str] = None
    GOOGLE_CLOUD_PROJECT_ID: Optional[str] = None
    GOOGLE_SERVICE_ACCOUNT_KEY: str = ""
    GOOGLE_SERVICE_ACCOUNT_KEY_PATH: str = ""
    
    def get_service_account_key(self):
        """Get service account key from file path or direct JSON string"""
        if self.GOOGLE_SERVICE_ACCOUNT_KEY_PATH:
            # Find the .env file location to determine project root
            env_file = find_dotenv()
            if env_file:
                project_root = Path(env_file).parent
            else:
                # Fallback to current working directory
                project_root = Path.cwd()
            
            # Try multiple possible paths for the service account key
            key_paths = [
                project_root / self.GOOGLE_SERVICE_ACCOUNT_KEY_PATH,  # Relative to project root
                Path(self.GOOGLE_SERVICE_ACCOUNT_KEY_PATH),  # Absolute path
                Path.cwd() / self.GOOGLE_SERVICE_ACCOUNT_KEY_PATH,  # Relative to current working directory
            ]
            
            for key_path in key_paths:
                if key_path.exists():
                    try:
                        with open(key_path, 'r') as f:
                            return json.load(f)
                    except Exception as e:
                        print(f"Error reading service account key file {key_path}: {e}")
                        continue
            
            print(f"Service account key file not found at any of these paths: {key_paths}")
            return None
        elif self.GOOGLE_SERVICE_ACCOUNT_KEY:
            try:
                return json.loads(self.GOOGLE_SERVICE_ACCOUNT_KEY)
            except Exception as e:
                print(f"Error parsing service account key JSON: {e}")
                return None
        return None

settings = Settings()