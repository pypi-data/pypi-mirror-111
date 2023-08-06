import requests
from requests.adapters import HTTPAdapter
from pygadgets import config
from dataclasses import dataclass
import logging
import time


BASEURL = "https://dane.biznes.gov.pl/api/ceidg/v1"

headers = {"Authorization": "Bearer " + config.PYGADGETS_CEIDG_API_TOKEN}

log = logging.getLogger(__name__)

_session = None
MAX_RETRIES = 3


class RequestError(Exception):
    pass


@dataclass
class Company:
    name: str
    address: dict
    status: str
    url: str
    details: dict


def get_session():
    global _session

    if _session is not None:
        log.debug("using cached session")
        return _session

    session = requests.Session()
    session.headers.update(headers)
    session.mount(prefix=BASEURL, adapter=HTTPAdapter(max_retries=MAX_RETRIES))
    _session = session
    return session


def make_request(query):
    time.sleep(0.1)
    log.info(f"making request: {query}")
    res = get_session().get(query)
    if res.status_code == 200:
        return res.json()
    else:
        raise RequestError(f"unable to make a request {str(res)}")


def get_page(num_page=1):
    url = BASEURL + f"/firmy?limit=50&page={num_page}".format(str(num_page))
    return make_request(url)


def expand_details(co):
    co.details = make_request(co.url)["firma"]
    return co


def prepare(raw_page, expand=False):
    companies = []
    for co in raw_page:
        c = Company(co["nazwa"], co["adresDzialanosci"], co["status"], co["link"], None)
        if expand:
            c = expand_details(c)
        companies.append(c)
    return companies


def iter_pages(numpages=None, expand=False, start_page=1):
    pagecount = 0
    page = get_page(start_page)
    while True:
        try:
            log.info(f"getting page {pagecount}")
            prepared = prepare(page["firmy"], expand)
            yield prepared
            next_link = page["links"]["next"]
            log.debug(f"next link {next_link}")
            page = make_request(next_link)
        except Exception as e:
            log.info(f"cannot get next page. ending. {str(e)}")
            break
        else:
            pagecount += 1
            if numpages and (pagecount >= numpages):
                log.info("maxpage reached. ending.")
                break
