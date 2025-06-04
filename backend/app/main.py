from fastapi import FastAPI
from app.api.router import api_router
from app.core.config import settings
from app.core.logging import setup_logging

setup_logging()

app = FastAPI(title="Realtor Planning App")

app.include_router(api_router)
print(settings.DATABASE_URL)

@app.get("/")
def root():
    return {"status": "OK", "message": "Realtor Planning API is live"}