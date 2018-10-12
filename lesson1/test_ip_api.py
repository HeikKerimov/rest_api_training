import api.ip_api as ip_api
from jsonschema import validate
from helpers.file import load_from_json


def test_schema():
    data = ip_api.get_data()
    ip_schema = load_from_json(folder="data", file="ip_schema")
    validate(data, ip_schema), "The schema is invalid"


def test_ip():
    data = ip_api.get_data()
    ip = data["query"]
    assert ip_api.check_ip(ip), "The IP is wrong"


def test_country():
    data = ip_api.get_data()
    country = data["country"]
    countries = load_from_json(folder="data", file="countries")
    assert any(c["Name"] == country for c in countries), "There is no the country"


def test_city():
    data = ip_api.get_data()
    city = data["city"]
    assert len(city) > 0, "City is empty"
    cities = load_from_json(folder="data", file="cities")
    assert any(c["name"] == city for c in cities), "There is no the city"


def test_lat():
    data = ip_api.get_data()
    lat = data["lat"]
    assert lat >= 0, "The Lat is less than 0"


def test_lon():
    data = ip_api.get_data()
    lon = data["lon"]
    assert lon >= 0, "The Lon is less than 0"
