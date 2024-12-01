from time import sleep


def get_help() -> None:
    text: str = (
        "Все доступные команды:\n"
        "/add_task - Добавить новую задачу\n"
        "/delete_task - Удалить задачу\n"
        "/find_task - Найти задачу(и)\n"
        "/update_task - Обновить существующую задачу\n"
        "/update_task_status - Обновить статус задачи\n"
        "/get_all_tasks - Показать все задачи\n"
        "/help - Посмотреть все команды\n"
        "/exit - Выход из программы"
    )
    print(text)


def exit_program() -> None:
    print("Выход из приложения.....")
    sleep(1)
