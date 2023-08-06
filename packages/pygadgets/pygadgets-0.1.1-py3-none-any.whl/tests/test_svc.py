import pytest

from pygadgets.svc import CeidgService


@pytest.fixture
def ceidg():
    return CeidgService()


def test_can_dump_to_datafiles(ceidg):
    ceidg.prepare_dump(numpages=1, clear=True)
    assert len(ceidg.datafiles) == 1
    

def test_can_list_datafiles(ceidg):
    assert len(ceidg.datafiles) > 0


def test_can_read_from_datafiles(ceidg):
    assert len(ceidg.pages) > 0


def test_can_list_companies_from_datafiles(ceidg):
    companies = ceidg.list_companies()
    assert len(companies) == 50



    