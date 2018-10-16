""" This module is about ip-api. """

import requests


BASE_URL = "http://ip-api.com/json"


def get_data():
    """ This method returns json data about ip. """

    response = requests.get(BASE_URL)
    return response.json()


def check_ip(ip_address):
    """ This method checks an ip is correct or not. """

    numbers = [int(n) for n in ip_address.split(".")]
    for number in numbers:
        if number <= 0 or number > 255:
            return False
        return True
