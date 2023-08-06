from pygadgets.ext.ceidg import get_companies
import pytest


# @pytest.mark.skip('skip for now')
def test_get_companies():
    assert len(get_companies()['firmy']) > 0