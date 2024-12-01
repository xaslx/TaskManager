from abc import ABC, abstractmethod


class BaseStorage(ABC):

    @abstractmethod
    def add(self, data: dict) -> None:
        """Добавить запись."""
        pass

    @abstractmethod
    def get_all(self) -> list[dict] | None:
        """Получить все записи."""
        pass

    @abstractmethod
    def get_one_or_none(self, id: int) -> dict | None:
        """Получить одну запись по фильтрам."""
        pass

    @abstractmethod
    def update(self, data: list[dict]) -> None:
        """Обновить записи."""
        pass

    @abstractmethod
    def delete(self, id: int) -> None:
        """Удалить записи по фильтрам."""
        pass
