from os.path import join
from os import makedirs, environ
from pathlib import Path
import logging
from dotenv import dotenv_values, load_dotenv
from io import StringIO

logging.basicConfig(level=logging.DEBUG)
LOG = logging.getLogger(__name__)
LOCAL_DIR = join(Path.home(), ".pygadget")

try:
    makedirs(LOCAL_DIR)
except OSError:
    LOG.info(".pygadget already exists. skipping.")
except Exception as e:
    raise RuntimeError(f"unhandled exceptions {str(e)}")
else:
    LOG.info(".pygadget dir created")


try:
    env = dotenv_values(stream=StringIO(open(join(LOCAL_DIR, ".env"), "r").read()))
    LOG.info("loaded vars from .env")
except OSError:
    env = {k: v for k, v in environ.items() if k.startswith("PYGADGETS")}
    LOG.info("loaded vars from environ")


if env == {}:
    raise RuntimeError('Unable to collect configuration vars')

config = type("Config", (), env)
