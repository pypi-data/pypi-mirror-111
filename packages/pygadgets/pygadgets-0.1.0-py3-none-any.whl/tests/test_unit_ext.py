from pygadgets.ext.ceidg import get_page, iter_pages
import pytest


# @pytest.mark.skip('skip for now')
def test_get_page():
    assert len(get_page()['firmy']) == 50

def test_iter_pages():
    pages = list(iter_pages(2))
    assert len(pages) == 2
    assert pages[0][0].details is None

def test_iter_pages_expanded():
    pages = list(iter_pages(numpages=1, expand=True))
    assert len(pages) == 1
    assert pages[0][0].details is not None




