from datetime import datetime
from enum import Enum
from src.models.task import Task, TaskCategory, TaskPriority, TaskStatus
from src.storage.json_storage import JsonStorage


class TaskManager:

    def __init__(self, database: JsonStorage) -> None:
        self.db = database

    def add_new_task(self):
        """Метод для добавления новой задачи"""

        task_title: str = input("Введите название задачи: ").strip()
        task_description: str = input("Введите описание задачи: ").strip()

        if len(task_title) < 3 or len(task_description) < 3:
            print("Название задачи и описание должны быть больше 3-ех символов!")
            return

        task_category: str = self._get_enum_input(
            "Введите категорию (Работа, Личное, Обучение): ", TaskCategory
        )
        due_date: str = self._format_date(input("Введите дату в формате ДД.ММ.ГГГГ: "))
        task_priority: str = self._get_enum_input(
            "Введите приоритет (Низкий, Средний, Высокий): ", TaskPriority
        )

        last_id: int = self._get_last_id()

        task: Task = Task(
            id=last_id + 1,
            title=task_title,
            description=task_description,
            category=task_category,
            due_date=due_date,
            priority=task_priority,
            status=TaskStatus.NOT_COMPLETED,
        )
        task_to_dict: dict = task.to_dict()
        self.db.add(data=task_to_dict)
        print("Новая задача успешно добавлена!")

    def update_status_task(self):
        """Обновление статуса задачи"""

        task_id: int = self._validate_input("Введите ID задачи: ")
        task: dict | None = self.db.get_one_or_none(id=task_id)

        if not task:
            print("Задача не найдена!")
            return

        if task["status"] == TaskStatus.COMPLETED:
            print("Задача уже выполнена.")

        else:
            task["status"] = TaskStatus.COMPLETED

            tasks: list[dict] | None = self._update_task(task=task)
            self.db.update(data=tasks)
            print("Статус задачи обновлен. (Задача выполнена)")

    def _update_task(self, task: dict) -> list[dict]:
        tasks: list[dict] | None = self.db.get_all()
        for index, t in enumerate(tasks):
            if t["id"] == task["id"]:
                tasks[index] = task
                return tasks

    def update_task(self):
        """Обновление задачи"""

        task_id: int = self._validate_input(
            "Введите ID задачи, которую хотите обновить: "
        )
        task: dict | None = self.db.get_one_or_none(id=task_id)

        if not task:
            print("Задача с таким ID не найдена.")
            return

        print(f"Текущие данные задачи:\n{task}")

        task["title"] = (
            input(
                f'Новое название задачи (текущее: "{task["title"]}", оставьте пустым, если не хотите изменять): '
            ).strip()
            or task["title"]
        )

        task["description"] = (
            input(
                f'Новое описание (текущее: "{task["description"]}", оставьте пустым, если не хотите изменять): '
            ).strip()
            or task["description"]
        )

        task["category"] = self._get_enum_input(
            f'Новая категория (текущая: {task["category"]}, оставьте пустым, если не хотите изменять): ',
            TaskCategory,
            task["category"],
        )

        due_date_input: str = input(
            f'Новая дата выполнения (текущая: {task["due_date"]}, оставьте пустым, если не хотите изменять): '
        ).strip()

        task["due_date"] = (
            self._format_date(due_date_input) if due_date_input else task["due_date"]
        )

        task["priority"] = self._get_enum_input(
            f'Новый приоритет (текущий: {task["priority"]}, оставьте пустым, если не хотите изменять): ',
            TaskPriority,
            task["priority"],
        )

        tasks: list[dict] | None = self._update_task(task=task)
        self.db.update(data=tasks)
        print("Задача успешно обновлена!")

    def delete_task(self):
        """Удаление задачи"""

        while True:

            print("Выберите способ удаления:")
            print("1. Удалить задачу по ID")
            print("2. Удалить все задачи по категории")
            print("3. Выйти")

            choice: str = input("Введите номер: ").strip()

            if choice == "1":

                task_id: int = self._validate_input("Введите ID задачи: ")
                task: dict | None = self.db.get_one_or_none(id=task_id)

                if task:
                    self.db.delete(id=task_id)
                    print("Задача удалена!")
                else:
                    print("Задача не найдена!")
                break

            elif choice == "2":

                category: str = input(
                    "Введите категорию для удаления задач (Работа, Личное, Обучение): "
                ).strip()

                if category not in TaskCategory:
                    print("Такой категории нет! Попробуйте снова.")
                    continue

                tasks_to_delete: list[dict] | None = self.db.get_all()
                tasks_to_delete = [
                    task for task in tasks_to_delete if task["category"] == category
                ]
                if tasks_to_delete:

                    for task in tasks_to_delete:
                        self.db.delete(id=task["id"])
                    print(f"Все задачи в категории '{category}' удалены!")

                else:

                    print(f"Задачи в категории '{category}' не найдены!")

                break

            elif choice == "3":
                print("Выход")
                break

            else:
                print("Неверный выбор, попробуйте снова.")

    def get_all_tasks(self) -> None:
        """Вывод всех задач"""

        tasks: list[dict] | None = self.db.get_all()

        if tasks:
            self._print_task(tasks)

        else:
            print("Задач не найдено!")

    def find_task(self) -> None:
        """Поиск задачи по критерию"""

        while True:

            options: dict[str, tuple] = {
                "1": ("Поиск задачи по ID", self._find_task_by_id),
                "2": (
                    "Поиск по ключевым словам (название или описание)",
                    self._find_task_by_keyword,
                ),
                "3": ("Поиск по статусу выполнения", self._find_task_by_status),
                "4": ("Поиск по категории", self._find_task_by_category),
                "5": ("Выход", None),
            }

            print("\nВыберите критерий для поиска:")

            for key, (param, _) in options.items():
                print(f"{key}. {param}")

            choice: str = input("Введите номер: ").strip()

            if choice == "5":
                print("Выход из поиска.")
                break

            elif choice in options:
                options[choice][1]()
                break

            else:
                print("Неверный выбор. Попробуйте снова.")

    def _find_task_by_keyword(self) -> None:
        """Поиск задач по ключевым словам в названии или описании."""

        keyword: str = input("Введите ключевое слово для поиска: ").lower()
        tasks: list[dict] | None = self.db.get_all()

        found_tasks: list[dict] = [
            task
            for task in tasks
            if keyword in task["title"].lower()
            or keyword in task["description"].lower()
        ]
        self._print_task(found_tasks)

    def _find_task_by_status(self) -> None:
        """Поиск задач по статусу выполнения."""

        print("\nСтатусы выполнения:")

        while True:

            status: str = input(
                "Введите статус из возможных: (Не выполнена / Выполнена): "
            ).strip()

            if status not in TaskStatus:
                print("Такого статуса нет!")
                continue

            tasks: list[dict] | None = self.db.get_all()
            found_tasks: list[dict] | None = [
                task for task in tasks if task["status"] == status
            ]
            self._print_task(found_tasks)
            break

    def _find_task_by_id(self) -> None:
        """Поиск задачи по ID"""

        task_id: int = self._validate_input("Введите ID задачи: ")
        task: dict | None = self.db.get_one_or_none(id=task_id)
        if task:
            self._task_details(task)
        else:
            print("Задача не найдена!")

    def _find_task_by_category(self) -> None:
        """Поиск задач по категории."""

        while True:

            print(
                "Введите название категории, чтобы найти все задачи из этой категории"
            )
            category: str = input("Доступные категории: (Работа, Личное, Обучение): ")

            if category not in TaskCategory:
                print("Такой категории нет!")
                continue

            all_tasks: list[dict] | None = self.db.get_all()
            all_tasks = [task for task in all_tasks if task["category"] == category]

            if not all_tasks:
                print("Задач не найдено!")
                break

            self._print_task(tasks=all_tasks)
            break

    def _validate_input(self, prompt: str) -> int:
        """Метод для валидации целого числа"""

        while True:
            try:
                return int(input(prompt).strip())
            except ValueError:
                print(f"Ошибка: ожидалось целое число (int)")

    def _get_enum_input(
        self, prompt: str, enum: Enum, default: str | None = None
    ) -> str:
        """Метод для проверки есть ли вводимое значение в допустимых"""

        while True:

            value: str = input(prompt).strip().capitalize()

            if not value and default:
                return default

            if value in enum:
                return value

            print(f'Ошибка: допустимые значения: {", ".join(enum)}.\n')

    def _format_date(self, date_str: str) -> str:
        """Метод для валидации даты"""

        while True:
            try:
                datetime.strptime(date_str, "%d.%m.%Y").date()
                return date_str
            except ValueError:
                print("Ошибка: неверный формат даты. Ожидается ДД.ММ.ГГГГ.")
                date_str = input("Введите дату в формате ДД.ММ.ГГГГ: ")

    def _print_task(self, tasks: list[dict] | None) -> None:

        if isinstance(tasks, list):
            if not tasks:
                print("Задач не найдено!")
                return
            for task in tasks:
                self._task_details(task)
        else:
            self._task_details(tasks)

    def _task_details(self, task: dict) -> None:
        """Вывод информации о задаче"""

        print(
            f"\nID: {task['id']}\n"
            f"Название: {task['title']}\n"
            f"Описание: {task['description']}\n"
            f"Категория: {task['category']}\n"
            f"Срок выполнения: {task['due_date']}\n"
            f"Приоритет: {task['priority']}\n"
            f"Статус: {task['status']}\n"
            f"---------------------"
        )

    def _get_last_id(self) -> int:
        """Метод для получения последнего ID"""

        tasks: list[dict] | None = self.db._load_tasks()
        return max(task["id"] for task in tasks) if tasks else 0
