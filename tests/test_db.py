import os
from src.storage.json_storage import JsonStorage
from src.models.task import Task


def test_create_db(db: JsonStorage):
    """Проверка, что база данных создается, если она не существует"""

    assert os.path.exists(db.filepath)


def test_add_task(db: JsonStorage, task: Task):
    """Добавление задачи в базу данных"""
    task_to_dict: dict = task.to_dict()
    db.add(task_to_dict)


def test_task_exist(db: JsonStorage):
    """Проверка что задача есть в базе данных"""

    tasks: list[dict] | None = db.get_all()
    assert len(tasks) == 1
    assert tasks[0]["title"] == "Task 1"


def test_find_task(db: JsonStorage):
    """Получение задачи"""

    task: dict | None = db.get_one_or_none(id=1)
    assert task


def test_delete_task(db: JsonStorage):
    """Удаление задачи"""

    db.delete(id=1)
    tasks: list[dict] = db.get_all()
    assert len(tasks) == 0
