from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Club(Base):
    __tablename__ = "clubs"

    club_id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.user_id"), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    lg_api_key: Mapped[str | None] = mapped_column(String(255), nullable=True)
    secret: Mapped[str | None] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    owner: Mapped["User"] = relationship("User", back_populates="owned_clubs", foreign_keys=[owner_id])
    users: Mapped[list["User"]] = relationship("User", back_populates="club", foreign_keys="User.club_id")
