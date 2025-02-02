import uuid

from typing import List
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base


class Accounts(Base):
    """
    Модель таблицы счетов пользователей.

    Колонки:
        - id            | Идентификатор
        - id_user       | Идентификатор пользователя - владельца счета
        - balance       | Баланс счета
    """

    __tablename__ = "Accounts"

    id:             Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    id_user:        Mapped[str] = mapped_column(String(36), ForeignKey('Users.id', ondelete='CASCADE'), nullable=False)
    balance:        Mapped[float] = mapped_column()

    conn_users: Mapped[List["Users": str]] = relationship("Users", back_populates="conn_users_account")
    conn_payments: Mapped[List["Payments": str]] = relationship("Payments", back_populates="conn_account")
