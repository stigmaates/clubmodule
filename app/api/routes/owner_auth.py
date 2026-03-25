from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.auth import OwnerLoginIn, OwnerRegisterIn
from app.services.auth_service import AuthService

router = APIRouter(prefix="/owner", tags=["Owner Auth"])
templates = Jinja2Templates(directory="app/templates")


@router.get("/auth", response_class=HTMLResponse)
def owner_auth_page(request: Request):
    return templates.TemplateResponse(
        request,
        "owner_auth.html",
        {"register_message": None, "login_message": None, "login_success": False},
    )


@router.post("/register", response_class=HTMLResponse)
def owner_register(
    request: Request,
    owner_name: str = Form(...),
    club_name: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db),
):
    register_message = ""
    try:
        payload = OwnerRegisterIn(owner_name=owner_name.strip(), club_name=club_name.strip(), password=password)
        user = AuthService.register_owner(db, payload)
        register_message = f"Владелец {user.name} и клуб созданы успешно."
    except ValueError as exc:
        register_message = str(exc)

    return templates.TemplateResponse(
        request,
        "owner_auth.html",
        {"register_message": register_message, "login_message": None, "login_success": False},
    )


@router.post("/login", response_class=HTMLResponse)
def owner_login(
    request: Request,
    name: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db),
):
    login_message = ""
    login_success = False
    try:
        payload = OwnerLoginIn(name=name.strip(), password=password)
        user = AuthService.authenticate_owner(db, payload)
        login_message = f"Добро пожаловать, {user.name}."
        login_success = True
    except ValueError as exc:
        login_message = str(exc)

    return templates.TemplateResponse(
        request,
        "owner_auth.html",
        {"register_message": None, "login_message": login_message, "login_success": login_success},
    )
