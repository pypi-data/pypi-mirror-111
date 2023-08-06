import requests
from pygadgets import config


BASEURL = "https://dane.biznes.gov.pl/api/ceidg/v1"

headers = {"Authorization": "Bearer " + config.PYGADGETS_CEIDG_API_TOKEN}


def get_companies():
    session = requests.Session()
    session.headers.update(headers)
    return session.get(BASEURL + "/firmy").json()
