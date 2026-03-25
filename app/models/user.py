from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class User(Base):
    __tablename__ = "users"

    user_id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    role: Mapped[str] = mapped_column(String(50), nullable=False, default="master_owner")
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    club_id: Mapped[int | None] = mapped_column(ForeignKey("clubs.club_id"), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    pass_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    last_activity: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    club: Mapped["Club"] = relationship("Club", back_populates="users", foreign_keys=[club_id])
    owned_clubs: Mapped[list["Club"]] = relationship("Club", back_populates="owner", foreign_keys="Club.owner_id")
