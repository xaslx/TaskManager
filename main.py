from src.service.task_manager import TaskManager
from src.storage.json_storage import JsonStorage
from src.utils.utils import get_help, exit_program
from typing import Callable


def main():

    json_storage: JsonStorage = JsonStorage(filepath="db.json")
    task_manager: TaskManager = TaskManager(database=json_storage)

    COMMANDS: dict[str, Callable[[], None]] = {
        "/add_task": task_manager.add_new_task,
        "/delete_task": task_manager.delete_task,
        "/find_task": task_manager.find_task,
        "/update_task": task_manager.update_task,
        "/update_task_status": task_manager.update_status_task,
        "/get_all_tasks": task_manager.get_all_tasks,
        "/help": get_help,
        "/exit": exit_program,
    }

    print('Приложение "Менеджер задач"')
    get_help()

    while True:
        command: str = input(
            "\nВведите одну из команд, или /help - чтобы посмотреть все доступные команды: "
        ).strip()
        function = COMMANDS.get(command)

        if not function:
            print(
                "Вы ввели неверную команду\nЧтобы посмотреть список команд - введите /help\n"
            )
        else:
            function()


if __name__ == "__main__":
    main()
