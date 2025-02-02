import uuid

from typing import List
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base


class Payments(Base):
    """
    Модель таблицы платежей пользователей.

    Колонки:
        - id            | Идентификатор
        - id_user       | Идентификатор пользователя
        - id_account    | Идентификатор счета назначения платежа
        - amount        | Сумма транзакции
        - signature     | Подпись транзакции
    """

    __tablename__ = "Payments"

    id:             Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    id_user:        Mapped[str] = mapped_column(String(36), ForeignKey('User_access_levels.id', ondelete='CASCADE'), nullable=False)
    id_account:     Mapped[str] = mapped_column(String(36), ForeignKey('Accounts.id', ondelete='CASCADE'), nullable=False)
    amount:         Mapped[float] = mapped_column()
    signature:      Mapped[str] = mapped_column(String(64))

    conn_users: Mapped[List["Users": str]] = relationship("Users", back_populates="conn_payments")
    conn_account: Mapped[List["Accounts": str]] = relationship("Accounts", back_populates="conn_payments")
