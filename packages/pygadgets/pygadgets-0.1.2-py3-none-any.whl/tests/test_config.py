from pygadgets import config, LOCAL_DIR
from os.path import exists, join


def test_config_vars():
    assert config.PYGADGETS_CEIDG_API_TOKEN is not None

def test_local_dirs_created():
    assert exists(LOCAL_DIR) is True
    assert exists(join(LOCAL_DIR, 'data'))






