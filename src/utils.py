import requests
import psycopg2
from src.config import config


def get_vacancies_list():
    """Получение списка словарей о вакансиях и компаниях"""
    url = 'https://api.hh.ru/vacancies'
    headers = {'User-Agent': 'HH-User-Agent'}
    items_list = []
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
