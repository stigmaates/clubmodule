from datetime import datetime

from passlib.context import CryptContext
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.club import Club
from app.models.user import User
from app.schemas.auth import OwnerLoginIn, OwnerRegisterIn

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthService:
    @staticmethod
    def register_owner(db: Session, payload: OwnerRegisterIn) -> User:
        existing = db.execute(select(User).where(User.name == payload.owner_name)).scalar_one_or_none()
        if existing:
            raise ValueError("Пользователь с таким именем уже существует")

        user = User(
            role="master_owner",
            name=payload.owner_name,
            pass_hash=pwd_context.hash(payload.password),
            created_at=datetime.utcnow(),
        )
        db.add(user)
        db.flush()

        club = Club(
            owner_id=user.user_id,
            name=payload.club_name,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )
        db.add(club)
        db.flush()

        user.club_id = club.club_id
        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def authenticate_owner(db: Session, payload: OwnerLoginIn) -> User:
        user = db.execute(select(User).where(User.name == payload.name)).scalar_one_or_none()
        if not user or not pwd_context.verify(payload.password, user.pass_hash):
            raise ValueError("Неверное имя или пароль")

        user.last_activity = datetime.utcnow()
        db.commit()
        db.refresh(user)
        return user
