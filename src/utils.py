import requests
import json
import psycopg2
from src.config import config


def get_response(user_input):
    """Получение списка словарей о вакансиях и компаниях"""
    url = 'https://api.hh.ru/vacancies'
    headers = {'User-Agent': 'HH-User-Agent'}
    param = {'text': user_input, 'page': 10, 'per_page': 50}
    response_json = requests.get(url, params=param, headers=headers)
    data_response = json.loads(response_json.text)['items']
    data_list = []
    for vacancy in data_response:
        vac_dict = {'name': vacancy['name'], 'company': vacancy['employer']['name'], 'city': vacancy['area']['name'],
                    'url': vacancy['alternate_url']}
        if vacancy.get('salary'):
            vac_dict['from'] = vacancy.get('salary').get('from')
            vac_dict['to'] = vacancy.get('salary').get('to')
            vac_dict['currency'] = vacancy['salary']['currency']
        data_list.append(vac_dict)
    return data_list


def upload_to_database(data_list):
    """Функция загружающая полученные данные в таблицу postgres"""
    params = config()
    with psycopg2.connect(**params) as conn:
        with conn.cursor() as cur:
            cur.execute("DROP TABLE IF EXISTS vacancies")
        conn.commit()
        with conn.cursor() as cur:
            cur.execute("CREATE TABLE IF NOT EXISTS vacancies"
                        "("
                        "id serial PRIMARY KEY, "
                        "name varchar(100) NOT NULL, "
                        "salary_from int, "
                        "salary_to int,"
                        "currency varchar(10), "
                        "company varchar(100) NOT NULL, city varchar(50), "
                        "url varchar(255)"
                        ")")
        conn.commit()
        with conn.cursor() as cur:
            insert = (f"INSERT INTO vacancies (name, salary_from, salary_to, currency, "
                      f"company, url) VALUES(%s, %s, %s, %s, %s, %s)")
            for data in data_list:
                #тут надо прописать ИФ для каждого случая с САЛАРИ!
                item_tuple = (data['name'], data['from'], data['to'], data['currency'],
                              data['company'], data['url'])
                cur.execute(insert, item_tuple)
            # item_tuple = (data_list[0]['name'], data_list[0]['salary_from'], data_list[0]['salary_to'], data_list[0]['currency'],
            #               data_list[0]['company'], data_list[0]['url'])
            # cur.execute(insert, item_tuple)
        conn.commit()
        with conn.cursor() as cur:
            # cur.execute(f"SELECT table_name FROM information_schema.tables "
            #             f"WHERE table_schema = 'public'")
            cur.execute("SELECT * FROM vacancies")
            rows = cur.fetchall()
            for row in rows:
                print(row)

data = get_response('строитель')
upload_to_database(data)
