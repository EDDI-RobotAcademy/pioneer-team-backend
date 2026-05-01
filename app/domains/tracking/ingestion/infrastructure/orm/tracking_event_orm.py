from datetime import datetime

from sqlalchemy import BigInteger, DateTime, Index, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.database.base import Base


class TrackingEventORM(Base):
    __tablename__ = "tracking_events"
    __table_args__ = (
        Index("ix_tracking_events_session_occurred", "session_id", "occurred_at"),
        Index("ix_tracking_events_occurred_at", "occurred_at"),
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    event_type: Mapped[str] = mapped_column(String(20), nullable=False)
    session_id: Mapped[str] = mapped_column(String(64), nullable=False)
    content_id: Mapped[str] = mapped_column(String(255), nullable=False)
    occurred_at: Mapped[int] = mapped_column(BigInteger, nullable=False)
    referral_id: Mapped[str | None] = mapped_column(String(64), nullable=True)
    received_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=False),
        nullable=False,
        server_default=func.now(),
    )
