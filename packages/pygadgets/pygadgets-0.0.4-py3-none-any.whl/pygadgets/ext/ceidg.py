import requests
from requests.adapters import HTTPAdapter
from pygadgets import config


BASEURL = "https://dane.biznes.gov.pl/api/ceidg/v1"

headers = {"Authorization": "Bearer " + config.PYGADGETS_CEIDG_API_TOKEN}


def get_companies():
    session = requests.Session()
    url = BASEURL + '/firmy'

    session.headers.update(headers)
    session.mount(prefix=BASEURL, adapter=HTTPAdapter(max_retries=3))
    return session.get(url).json()
