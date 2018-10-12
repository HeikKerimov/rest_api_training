import requests


BASE_URL = "http://ip-api.com/json"


def get_data():
    response = requests.get(BASE_URL)
    return response.json()


def check_ip(ip):
    numbers = [int(n) for n in ip.split(".")]
    for number in numbers:
        if number <= 0 or number > 255:
            return False
        return True
