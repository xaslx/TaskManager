import os
import pytest
from src.service.task_manager import TaskManager
from src.storage.json_storage import JsonStorage
from src.models.task import Task


@pytest.fixture(scope="session")
def db():
    """Создает тестовую базу данных и удаляет ее после теста."""

    db_path: str = "test_db.json"
    if os.path.exists(db_path):
        os.remove(db_path)
    db: JsonStorage = JsonStorage(filepath=db_path)
    yield db
    os.remove(db_path)


@pytest.fixture(scope="session")
def task():
    """Возвращает экземпляр Task."""

    return Task(
        id=1,
        title="Task 1",
        description="Test Task",
        category="Работа",
        due_date="01.01.2024",
        priority="Средний",
        status="Не выполнена",
    )
