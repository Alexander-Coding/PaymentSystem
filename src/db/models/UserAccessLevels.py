import uuid

from typing import List
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base


class UserAccessLevels(Base):
    """
    Модель таблицы ролей пользователей.

    Колонки:
        - id        | Идентификатор
        - role      | Название роли
    """

    __tablename__ = "User_access_levels"

    id:     Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    role:   Mapped[str] = mapped_column(String(30), unique=True)

    conn_users: Mapped[List["Users": str]] = relationship("Users", back_populates="conn_access_levels", cascade="all, delete-orphan")
