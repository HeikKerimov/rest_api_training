import requests
from requests.auth import HTTPBasicAuth

from helpers.randomizer import get_random_value

USER = 'test_user'
PASSWORD = 'test_password'
HOST = 'http://0.0.0.0:7000'


def auth_cookie():
    """ This method allows to get auth cookie. """

    url = '{0}/login'.format(HOST)
    result = requests.get(url, auth=HTTPBasicAuth(USER, PASSWORD))
    data = result.json()

    return {'my_cookie': data['auth_cookie']}


def check_auth_cookie(cookie):
    cookies = cookie.split("-")
    if len(cookies) == 5:
        return True
    return False


def get_books():
    """ This method returns a list of books. """

    url = "{0}/books".format(HOST)
    result = requests.get(url, cookies=auth_cookie())
    books = result.json()
    return books


def list_is_empty():

    return len(get_books()) == 0


def add_book():
    """ This method creates a book. """

    url = "{0}/add_book".format(HOST)
    book = {"title": get_random_value(), "author": get_random_value()}

    # Send POST request to add a book:
    requests.post(url, data=book, cookies=auth_cookie())