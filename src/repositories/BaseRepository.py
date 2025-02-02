from abc import ABC, abstractmethod
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional, Dict, Generic, TypeVar


TCreateSchema = TypeVar('TSchema')
TReturnSchema = TypeVar('TReturnSchema')


class BaseRepository(Generic[TCreateSchema, TReturnSchema], ABC):
    @abstractmethod
    def __init__(self, db: AsyncSession) -> None:
        self._db = db

    @abstractmethod
    async def create(self, data: TCreateSchema) -> TReturnSchema:
        """Создать новую запись в таблице"""
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, id: int) -> Optional[TReturnSchema]:
        """Получить строку таблицы по id"""
        raise NotImplementedError

    @abstractmethod
    async def get_all(self) -> List[TReturnSchema]:
        """Получить всю таблицу"""
        raise NotImplementedError

    @abstractmethod
    async def get_list_by_filtered(self, filters: Dict[str, any]) -> List[TReturnSchema]:
        """
            Получить строки таблицы по фильтру.
            На выходе всегда список, возможно пустой.
            Фильтр представляет собой словарь.
            Каждый ключ - название столбца для фильтрации.
            Значение:
                1) Конкретное значение, которому должно быть равно значение в указанном в ключе столбце.
                2) Кортеж, где первый элемент - строка условный оператор, второй - значение.
            Пример:
            {
                'column_1': 10 - будут выбраны строки, где значение column_1 равно 10,
                'column_2': ('<=', 15) - будут выбраны строки, где column_2 <= 15
            }
        """
        raise NotImplementedError

    async def get_first_or_none_by_filtered(self, filters: Dict[str, any]) -> Optional[TReturnSchema]:
        """
            Получает записи по заданным фильтрам.
            На выходе всегда первый элемент или None, если ничего не найдено.
            Фильтр представляет собой словарь.
            Каждый ключ - название столбца для фильтрации.
            Значение:
                1) Конкретное значение, которому должно быть равно значение в указанном в ключе столбце.
                2) Кортеж, где первый элемент - строка условный оператор, второй - значение.
            Пример:
            {
                'column_1': 10 - будут выбраны строки, где значение column_1 равно 10,
                'column_2': ('<=', 15) - будут выбраны строки, где column_2 <= 15
            }
        """

        result = await self.get_list_by_filtered(filters)

        if len(result) == 0:
            return None

        return result[0]

    @abstractmethod
    async def update(self, id: int, updated_data: TCreateSchema) -> Optional[TReturnSchema]:
        """Обновить строку таблицы по id."""
        raise NotImplementedError

    async def delete(self, id: int) -> bool:
        """Удалить строку таблицы по id."""
        record = await self.get_by_id(id)

        if record:
            await self._db.delete(record)
            await self._db.commit()

            return True

        return False


__all__ = [
    'BaseRepository'
]
