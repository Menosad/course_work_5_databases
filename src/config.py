from configparser import ConfigParser
import os

path_to_database = os.path.join('..', 'data', 'database.ini')


def config(file_name=path_to_database, section='postgres'):
    parser = ConfigParser()
    parser.read(file_name)

    try:
        params = parser.items(section)
        db = {}
        for param in params:
            db[param[0]] = param[1]
        return db
    except:
        print(f"Error")
