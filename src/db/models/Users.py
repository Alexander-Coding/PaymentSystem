import uuid

from typing import List
from datetime import datetime
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base


class Users(Base):
    """
    Модель таблицы пользователей.

    Колонки:
        - id            | Идентификатор
        - id_role       | Идентификатор роли пользователя
        - username      | Логин
        - firstname     | Имя
        - lastname      | Фамилия
        - fatherhood    | Отчество
        - password_hash | Хешированный пароль
        - created_at    | Дата и время регистрации
        - email         | Адрес электронной почты
    """

    __tablename__ = "Users"

    id:             Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    id_role:        Mapped[str] = mapped_column(String(36), ForeignKey('User_access_levels.id', ondelete='CASCADE'), nullable=False)
    username:       Mapped[str] = mapped_column(String(30), unique=True)
    firstname:      Mapped[str] = mapped_column(String(30), nullable=True)
    lastname:       Mapped[str] = mapped_column(String(30), nullable=True)
    fatherhood:     Mapped[str] = mapped_column(String(30), nullable=True)
    password_hash:  Mapped[str] = mapped_column(String(97))
    email:          Mapped[str] = mapped_column(String(50), nullable=True)
    created_at:     Mapped[datetime] = mapped_column(default=datetime.now().replace(microsecond=0))

    conn_access_levels: Mapped[List["UserAccessLevels"]: str] = relationship("UserAccessLevels", back_populates="conn_users")
    conn_payments: Mapped[List["Payments"]: str] = relationship("Payments", back_populates="conn_users", cascade="all, delete-orphan")
