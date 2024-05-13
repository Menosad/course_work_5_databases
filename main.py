from src.utils import get_response, upload_to_database


def main():
    """Логика основного скрипта
    -- обновляет / формирует таблицу по запросу для каждого запроса отдельно"""

    print(f"Приветствую!\nВакансия для сбора данны:")
    user_input = input().lower().strip()
    data = get_response(user_input)
    upload_to_database()
    pass


if __name__ == '__main__':
    pass
