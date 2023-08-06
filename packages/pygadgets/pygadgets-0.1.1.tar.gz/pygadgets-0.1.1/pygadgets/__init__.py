from os.path import join
from os import makedirs, environ
from pathlib import Path
import logging
from dotenv import dotenv_values, load_dotenv
from io import StringIO

logging.basicConfig(level=logging.INFO)
LOG = logging.getLogger(__name__)
LOCAL_DIR = join(Path.home(), ".pygadgets")


def try_make_dirs(directory):
    try:
        makedirs(directory)
    except OSError:
        LOG.info(f"{directory} already exists. skipping.")
    except Exception as e:
        raise RuntimeError(f"unhandled exceptions {str(e)}")
    else:
        LOG.info(".pygadget dir created")


try_make_dirs(LOCAL_DIR)
try_make_dirs(join(LOCAL_DIR, "data"))

try:
    env = dotenv_values(stream=StringIO(open(join(LOCAL_DIR, ".env"), "r").read()))
    LOG.info("loaded vars from .env")
except OSError:
    env = {k: v for k, v in environ.items() if k.startswith("PYGADGETS")}
    LOG.info("loaded vars from environ")


if env == {}:
    raise RuntimeError("Unable to collect configuration vars")

config = type("Config", (), env)
