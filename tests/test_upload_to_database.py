import pytest
from src.utils import upload_to_database

def test_upload_to_database():
    lst = []
    assert upload_to_database(lst) == {'host': 'localhost', 'dbname': 'postgres', 'user': 'postgres', 'password': '1337'}