import logging
from types import ClassMethodDescriptorType
import requests
from requests.adapters import HTTPAdapter


log = logging.getLogger(__name__)


class RequestError(Exception):
    pass


class SessionHandler:
    _cache = {}

    @classmethod
    def get_session(cls, prefix, headers, retries=1):
        if prefix in cls._cache:
            log.debug(f"using cached session for {prefix}")
            return cls._cache[prefix]
        else:
            log.debug(f"creating new session for {prefix}")
            session = requests.Session()
            session.headers.update(headers)
            session.mount(prefix=prefix, adapter=HTTPAdapter(max_retries=retries))
            cls._cache[prefix] = session
            return session

    @classmethod
    def make_request(cls, session, url):
        log.info(f"making request: {url}")
        res = session.get(url)
        if res.status_code == 200:
            return res.json()
        else:
            raise RequestError(f"unable to make a request {str(res)}")


class lazyproperty:
    def __init__(self, func):
        self.func = func

    def __get__(self, instance, cls):
        if instance is None:
            return self
        else:
            value = self.func(instance)
            setattr(instance, self.func.__name__, value)
            return value
