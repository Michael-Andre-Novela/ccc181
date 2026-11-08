from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import (
    Boolean,
    CheckConstraint,
    DateTime,
    ForeignKey,
    String,
    func,
    true,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship


db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120))
    email: Mapped[str] = mapped_column(String(120), unique=True)
    role: Mapped[str] = mapped_column(
        String(20),
        default="passenger",
        server_default="passenger",
    )

    tickets: Mapped[list["Ticket"]] = relationship(back_populates="user")

    __table_args__ = (
        CheckConstraint(
            "role IN ('passenger', 'staff')",
            name="ck_users_role",
        ),
    )


class Service(db.Model):
    __tablename__ = "services"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True)
    avg_minutes: Mapped[int] = mapped_column(
        default=10,
        server_default="10",
    )
    active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        server_default=true(),
    )

    tickets: Mapped[list["Ticket"]] = relationship(back_populates="service")

    __table_args__ = (
        CheckConstraint(
            "avg_minutes > 0",
            name="ck_services_avg_minutes",
        ),
    )


class Ticket(db.Model):
    __tablename__ = "tickets"

    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="RESTRICT")
    )
    service_id: Mapped[int] = mapped_column(
        ForeignKey("services.id", ondelete="RESTRICT")
    )

    flight_number: Mapped[str] = mapped_column(String(12))
    pnr: Mapped[str] = mapped_column(String(6))
    bag_count: Mapped[int] = mapped_column()

    preferred_slot_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True)
    )

    priority_verified: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        server_default="false",
    )

    status: Mapped[str] = mapped_column(
        String(20),
        default="waiting",
        server_default="waiting",
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    called_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True)
    )

    user: Mapped["User"] = relationship(back_populates="tickets")
    service: Mapped["Service"] = relationship(back_populates="tickets")

    __table_args__ = (
        CheckConstraint(
            "char_length(pnr) = 6",
            name="ck_tickets_pnr_length",
        ),
        CheckConstraint(
            "bag_count BETWEEN 1 AND 5",
            name="ck_tickets_bag_count",
        ),
        CheckConstraint(
            "status IN ('waiting', 'called', 'served', 'no-show', 'left')",
            name="ck_tickets_status",
        ),
    )