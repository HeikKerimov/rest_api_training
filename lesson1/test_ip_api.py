import pytest
import requests
import json
from jsonschema import validate


def check_ip(ip):
    numbers = [int(n) for n in ip.split(".")]
    for number in numbers:
        if number < 0 or number > 255:
            return False
        return True


class TestIpAPI:

    @pytest.fixture(scope="function", autouse=True)
    def pre_and_post_conditions(self):
        self.data = requests.get("http://ip-api.com/json").json()

    def test_schema(self):
        with open("../data/ip_schema.json") as json_data:
            ip_schema = json.load(json_data)
        validate(self.data, ip_schema)

    def test_ip(self):
        ip = self.data["query"]
        assert check_ip(ip), "IP is wrong"

    def test_country(self):
        country = self.data["country"]
        assert len(country) > 0, "Country is empty"

    def test_city(self):
        city = self.data["city"]
        assert len(city) > 0, "City is empty"

    def test_lat(self):
        lat = self.data["lat"]
        assert lat >= 0, "Lat is less than 0"

    def test_lon(self):
        lon = self.data["lon"]
        assert lon >= 0, "Lon is less than 0"
