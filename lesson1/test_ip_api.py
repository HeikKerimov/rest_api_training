""" There are tests for ip-api.com in the module. """

import pytest
from jsonschema import validate
import api.ip_api as ip
from helpers.file import load_from_json


def test_schema():
    """ This test checks a json schema is correct. """

    data = ip.get_data()
    ip_schema = load_from_json(folder="data", file="ip_schema")
    validate(data, ip_schema)


def test_ip():
    """ This test checks an ip address is valid. """

    data = ip.get_data()
    ip_address = data["query"]
    assert ip.check_ip(ip_address), "The IP is wrong"


def test_country():
    """ This test checks that a country is in list of countries. """

    data = ip.get_data()
    country = data["country"]
    countries = load_from_json(folder="data", file="countries")
    assert any(c["Name"] == country for c in countries), "There is no the country"


def test_city():
    """ This test checks that a city is in list of cities. """
    data = ip.get_data()
    city = data["city"]
    cities = load_from_json(folder="data", file="cities")
    assert any(c["name"] == city for c in cities), "There is no the city"


def test_lat():
    """ This test checks that a latitude is more that 0. """

    data = ip.get_data()
    lat = data["lat"]
    assert lat >= 0, "The Lat is less than 0"


def test_lon():
    """ This test checks that a longitude is more that 0. """

    data = ip.get_data()
    lon = data["lon"]
    assert lon >= 0, "The Lon is less than 0"


if __name__ == "__main__":
    # в PyCharm удобно запускать как обычный скрипт. Без командной строки
    pytest.main()
