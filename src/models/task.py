from dataclasses import dataclass
from enum import StrEnum
from datetime import date


class TaskCategory(StrEnum):
    WORK = "Работа"
    PERSONAL = "Личное"
    EDUCATION = "Обучение"


class TaskPriority(StrEnum):
    LOW = "Низкий"
    MEDIUM = "Средний"
    HIGH = "Высокий"


class TaskStatus(StrEnum):
    COMPLETED = "Выполнена"
    NOT_COMPLETED = "Не выполнена"


@dataclass(frozen=True, slots=True)
class Task:
    id: int
    title: str
    description: str
    category: TaskCategory
    due_date: date
    priority: TaskPriority
    status: TaskStatus

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "category": self.category,
            "due_date": self.due_date,
            "priority": self.priority,
            "status": self.status,
        }
