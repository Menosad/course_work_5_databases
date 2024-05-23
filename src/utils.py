import requests
import psycopg2
from src.class_DBManager import DBManager
from src.config import config
import os


def get_vacancies_list():
    """Получение списка словарей о вакансиях и компаниях"""
    url = 'https://api.hh.ru/vacancies'
    headers = {'User-Agent': 'HH-User-Agent'}
    items_list = []
    print(f"Загружаю данные с сайта hh.ru...")
    for i in range(19):
        param = {'page': i+1, 'per_page': 20}
        response_json = requests.get(url, params=param, headers=headers).json()
        items_list.extend(response_json['items'])
    vacancies_list = []
    for vacancy in items_list:
        vac_dict = {'name': vacancy['name'], 'company': vacancy['employer']['name'], 'city': vacancy['area']['name'],
                    'url': vacancy['alternate_url']}
        if vacancy.get('salary'):
            vac_dict['from'] = vacancy.get('salary').get('from')
            vac_dict['to'] = vacancy.get('salary').get('to')
            vac_dict['currency'] = vacancy['salary']['currency']
        else:
            vac_dict['from'] = vacancy.get('salary')
            vac_dict['to'] = vacancy.get('salary')
            vac_dict['currency'] = vacancy.get('salary')
        vacancies_list.append(vac_dict)
    return vacancies_list


def upload_to_database(data_list: list, params):
    """Функция загружающая полученные данные в базу даных postgres в таблицу vacancies"""
    conn = psycopg2.connect(**params)
    print(f"Заношу данные в таблицу...")
    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute("DROP TABLE IF EXISTS vacancies")
                cur.execute("CREATE TABLE IF NOT EXISTS vacancies"
                            "("
                            "id serial PRIMARY KEY, "
                            "name varchar(255) NOT NULL, "
                            "salary_from int, "
                            "salary_to int,"
                            "currency varchar(10), "
                            "company varchar(255) NOT NULL, "
                            "url varchar(255)"
                            ")")
                insert = (f"INSERT INTO vacancies (name, salary_from, salary_to, currency, "
                          f"company, url) VALUES(%s, %s, %s, %s, %s, %s)")
                for vac in data_list:
                    item_tuple = (vac['name'], vac['from'], vac['to'], vac['currency'],
                                  vac['company'], vac['url'])
                    cur.execute(insert, item_tuple)
        print(f"Данные успешно загруженны")
    finally:
        conn.close()

def information_output():
    path_to_config = os.path.join('data', 'database.ini')
    par = config(path_to_config)
    dbman = DBManager(par)
    commands = ('companies', 'vacancies', 'avg_salary',
                'higher_salary', 'keyword', 'stop')
    command = ''
    while True:
        print(f"\nВыберите команду:\n")
        print(f"companies - выводит список всех компаний и \nколичество вакансий у каждой компании;\n"
              f"vacancies - получает список всех вакансий с указанием названия компании, \nназвания вакансии и зарплаты и ссылки на вакансию;\n"
              f"avg_salary - получает среднюю зарплату по вакансиям;\n"
              f"higher_salary - получает список всех вакансий, у которых \nзарплата выше средней по всем вакансиям;\n"
              f"keyword - получает список всех вакансий, в названии которых \nсодержатся переданные в метод слова, например python;\n"
              f"stop - завершает работу приложения.")
        command = input().lower().strip()
        if command not in commands:
            print(f"\nТАКОЙ КОМАНДЫ НЕТ!\n")
        else:
            if command == 'companies':
                dbman.get_companies_and_vacancies_count()
            elif command == 'vacancies':
                dbman.get_all_vacancies()
            elif command == 'avg_salary':
                dbman.get_avg_salary()
            elif command == 'higher_salary':
                dbman.get_vacancies_with_higher_salary()
            elif command == 'keyword':
                dbman.get_vacancies_with_keyword()
            elif command == 'stop':
                print(f"Работа завершена!")
                quit()
