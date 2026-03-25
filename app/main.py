from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.api.routes.owner_auth import router as owner_auth_router
from app.core.config import settings

app = FastAPI(title=settings.app_name, debug=settings.debug)
app.mount("/static", StaticFiles(directory="app/static"), name="static")
app.include_router(owner_auth_router)
