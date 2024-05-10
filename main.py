from src.config import config
from src.utils import get_response


def main():
    """Логика основного скрипта
    -- обновляет / формирует таблицу по запросу для каждого запроса отдельно"""

    print(f"Приветствую!\nВакансия для сбора данны:")
    user_input = input().lower().strip()
    data = get_response(user_input)
    get_params = config()
    pass


if __name__ == '__main__':
    pass
