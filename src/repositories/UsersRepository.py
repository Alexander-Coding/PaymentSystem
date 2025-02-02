from sqlalchemy import and_
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, Dict, Any, List

from src.db.models import Users, UserAccessLevels
from src.repositories import BaseRepository
from src.db.schemas import UserResponseSchema, UserCreateSchema


class UsersRepository(BaseRepository[UserCreateSchema, UserResponseSchema]):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, data: UserCreateSchema) -> Users:
        """Создает новую запись в таблице Users."""
        user_db = Users(**data.dict())
        self.db.add(user_db)

        await self.db.commit()
        await self.db.refresh(user_db)

        return user_db

    async def get_by_id(self, id: int) -> Optional[UserResponseSchema]:
        """Получает запись по идентификатору."""
        result = await self.db.execute(
            select(
                Users.id,
                Users.id_role,
                Users.username,
                Users.firstname,
                Users.lastname,
                Users.fatherhood,
                Users.password_hash,
                Users.email,
                Users.created_at,
                UserAccessLevels.role
            )
            .join(Users.conn_access_levels)
            .where(Users.id == id)
        )

        row = result.first()
        row_dict = row._asdict()

        return UserResponseSchema(**row_dict)

    async def get_all(self) -> List[UserResponseSchema]:
        """Получает все записи из таблицы."""
        result = await self.db.execute(
            select(
                Users.id,
                Users.id_role,
                Users.username,
                Users.firstname,
                Users.lastname,
                Users.fatherhood,
                Users.password_hash,
                Users.email,
                Users.created_at,
                UserAccessLevels.role
            )
            .join(Users.conn_access_levels)
        )
        rows = result.all()

        formatted_result = []

        for row in rows:
            row_dict = row._asdict()
            formatted_result.append(UserResponseSchema(**row_dict))

        return formatted_result or []

    async def get_list_by_filtered(self, filters: Dict[str, Any]) -> List[UserResponseSchema]:
        """
            Получает записи по заданным фильтрам.
            На выходе всегда список, возможно пустой.
            :param filters: Словарь с условиями фильтрации.
                Словарь имеет структуру:
                    'Название колонки для фильтрации': <условие фильтрации>.
                    Условие фильтрации либо значение, которому равно значение в указанной колонке,
                    либо картеж, где первый элемент - условный оператор, второй - значение.
                Пример:
                {
                    'username': ('==', 'admin'),
                    'email': example@example.com
                }
            :return: Список записей, соответствующих фильтрам.
        """

        query = select(
            Users.id,
            Users.id_role,
            Users.username,
            Users.firstname,
            Users.lastname,
            Users.fatherhood,
            Users.password_hash,
            Users.email,
            Users.created_at,
            UserAccessLevels.role
        ).join(Users.conn_access_levels)

        conditions = []

        for key, value in filters.items():
            if hasattr(Users, key):
                if isinstance(value, tuple) and len(value) == 2:
                    operator, comparison_value = value

                    if operator == '==':
                        conditions.append(getattr(Users, key) == comparison_value)

                    elif operator == '!=':
                        conditions.append(getattr(Users, key) != comparison_value)

                    elif operator == '>':
                        conditions.append(getattr(Users, key) > comparison_value)

                    elif operator == '<':
                        conditions.append(getattr(Users, key) < comparison_value)

                    elif operator == '>=':
                        conditions.append(getattr(Users, key) >= comparison_value)

                    elif operator == '<=':
                        conditions.append(getattr(Users, key) <= comparison_value)

                    elif operator == 'in':
                        conditions.append(getattr(Users, key).in_(comparison_value))

                    elif operator == 'is':
                        conditions.append(getattr(Users, key).is_(comparison_value))

                    elif operator == 'is not':
                        conditions.append(getattr(Users, key).is_not(comparison_value))

                else:
                    conditions.append(getattr(Users, key) == value)

        if conditions:
            query = query.where(and_(*conditions))

        result = await self.db.execute(query)

        rows = result.all()

        formatted_result = []

        for row in rows:
            row_dict = row._asdict()
            formatted_result.append(UserResponseSchema(**row_dict))

        return formatted_result or []

    async def update(self, id: int, updated_data: UserResponseSchema) -> Optional[UserResponseSchema]:
        """
            Обновляет запись по идентификатору.
            Возвращает обновленное значение, или None, если запись для обновления не найдена.
        """

        user_record = await self.get_by_id(id)

        if user_record:
            for key, value in updated_data.__dict__.items():
                if key != "_sa_instance_state":
                    setattr(user_record, key, value)

            await self.db.commit()
            await self.db.refresh(user_record)

            return user_record

        return None


__all__ = [
    'UsersRepository',
    'UserResponseSchema'
]
