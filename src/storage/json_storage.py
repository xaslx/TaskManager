import json
import os
from src.storage.base_storage import BaseStorage


class JsonStorage(BaseStorage):

    def __init__(self, filepath: str) -> None:
        self.filepath = filepath

        # При запуске программы создается база данных, если она еще не создана
        if not os.path.exists(self.filepath):
            self._create_db()
            print("База данных создана")

    def _create_db(self) -> None:
        """Метод для создания базы данных"""

        try:
            with open(self.filepath, "w", encoding="utf-8") as file:
                json.dump([], file, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"Ошибка при создании базы данных: {e}")

    def _load_tasks(self) -> list[dict] | None:
        """Метод для получения всех задач"""

        try:
            with open(self.filepath, encoding="utf-8") as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def _save_to_file(self, tasks: list[dict]) -> None:
        """Метод для сохранения данных в базе"""

        try:
            with open(self.filepath, "w", encoding="utf-8") as file:
                json.dump(tasks, file, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"Ошибка при сохранении данных: {e}")

    def add(self, data: dict) -> None:
        tasks: list[dict] = self._load_tasks()
        tasks.append(data)
        self._save_to_file(tasks)

    def get_one_or_none(
        self,
        id: int,
    ) -> dict | None:
        """Метод для получения одного обьекта"""

        tasks: list[dict] | None = self._load_tasks()
        if tasks:
            for task in tasks:
                if task["id"] == id:
                    return task
        return None

    def get_all(self) -> list[dict] | None:
        """Метод для получения всех обьектов"""

        all_tasks: list[dict] | None = self._load_tasks()
        return all_tasks

    def update(self, data: list[dict]) -> None:
        """Метод для обновления данных"""

        self._save_to_file(tasks=data)

    def delete(self, id: int) -> None:
        """Метод для удаления обьекта"""

        tasks: list[dict] = self._load_tasks()

        if tasks:
            new_list: list[dict] = [task for task in tasks if task["id"] != id]
            self._save_to_file(tasks=new_list)

        return None
