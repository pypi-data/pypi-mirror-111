



import os
from os.path import join
from os import makedirs
from pathlib import Path
import logging

LOG = logging.getLogger(__name__)


try:
    makedirs(join(Path.home(), '.pygadget'))
except OSError:
    LOG.info('.pygadget already exists. skipping.')
except Exception as e:
    raise RuntimeError(f'unhandled exceptions {str(e)}')
else:
    LOG.info('.pygadget dir created')




    


