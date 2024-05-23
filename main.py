from src.utils import get_vacancies_list, upload_to_database
from src.class_DBManager import DBManager
from src.config import config
import os


path_to_file = os.path.join('data', 'database.ini')
par = config(path_to_file)
# vacancies_list = get_vacancies_list()
# upload_to_database(vacancies_list, par)
dbman = DBManager(par)
word = input(f"Введите название вакансии: ")
dbman.get_vacancies_with_keyword(word)

