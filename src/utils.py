import requests
import json
import psycopg2


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
                    'url': vacancy['employer']['alternate_url']}
        if vacancy.get('salary'):
            vac_dict['from'] = vacancy.get('salary').get('from')
            vac_dict['to'] = vacancy.get('salary').get('to')
        data_list.append(vac_dict)
    return data_list


