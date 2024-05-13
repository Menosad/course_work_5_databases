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
        else:
            vac_dict['from'] = vacancy.get('salary')
            vac_dict['to'] = vacancy.get('salary')
            vac_dict['currency'] = vacancy.get('salary')

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
                item_tuple = (data['name'], data['from'], data['to'], data['currency'],
                              data['company'], data['url'])
                cur.execute(insert, item_tuple)

        conn.commit()
        with conn.cursor() as cur:
            # cur.execute(f"SELECT table_name FROM information_schema.tables "
            #             f"WHERE table_schema = 'public'")
            cur.execute("SELECT * FROM vacancies")
            rows = cur.fetchall()
            for row in rows:
                print(row)


class DBManager:
    __slots__ = ['final_data']

    def __init__(self):
        self.final_data = []

    def get_companies_and_vacancies_count(self):
        """получает список всех компаний и количество вакансий у каждой компании"""
        headers = {'User-Agent': 'HH-User-Agent'}
        url = 'https://api.hh.ru/vacancies'
        for num, i in enumerate(range(19)):
            params = {'per_page': 110, 'page': i}
            response = requests.get(url, headers=headers, params=params)
            vacancies_list = json.loads(response.text)['items']
            self.final_data.extend(vacancies_list)
        return self.final_data, len(self.final_data)

    def get_all_vacancies(self):
        """получает список всех вакансий с указанием названия компании,
        названия вакансии и зарплаты и ссылки на вакансию"""
        vacancies_list = []
        for vacancy in self.final_data:
            vac_dict = {'company': vacancy['employer']['name'], 'name': vacancy['name'], 'url': vacancy['alternate_url']}
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


    def get_avg_salary(self):
        """получает среднюю зарплату по вакансиям"""
        pass
    def get_vacancies_with_higher_salary(self):
        """получает список всех вакансий, у которых зарплата выше средней по всем вакансиям"""
        pass
    def get_vacancies_with_keyword(self):
        """получает список всех вакансий, в названии которых содержатся переданные в метод слова,
         например python"""
        pass


dbmanager = DBManager()
dbmanager.get_companies_and_vacancies_count()
data = dbmanager.get_all_vacancies()
print(data[0])
