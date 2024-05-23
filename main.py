from src.utils import get_vacancies_list, upload_to_database
from src.class_DBManager import DBManager
from src.config import config
import os


def main():
    path_to_file = os.path.join('data', 'database.ini')
    par = config(path_to_file)
    vacancies_list = get_vacancies_list()
    upload_to_database(vacancies_list, par)
    dbman = DBManager(par)
    commands = {
        'companies': dbman.get_companies_and_vacancies_count(),
        'vacancies': dbman.get_all_vacancies(),
        'avg_salary': dbman.get_avg_salary(),
        'higher_salary': dbman.get_vacancies_with_higher_salary(),
        'keyword': dbman.get_vacancies_with_keyword(),
        'stop': quit()
    }
    command = ''
    while command != 'stop':
        print(f"Команды для работы с приложением:"
              f"companies - выводит список всех компаний и \nколичество вакансий у каждой компании;"
              f"vacancies - получает список всех вакансий с указанием названия компании, \nназвания вакансии и зарплаты и ссылки на вакансию;"
              f"avg_salary - получает среднюю зарплату по вакансиям;"
              f"higher_salary - получает список всех вакансий, у которых \nзарплата выше средней по всем вакансиям;"
              f"keyword - получает список всех вакансий, в названии которых \nсодержатся переданные в метод слова, например python;"
              f"stop - завершает работу приложения.")
        command = input().lower().strip()
        if command in commands:
            commands.get(command)


if __name__ == '__main__':
    main()
