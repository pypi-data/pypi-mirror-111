import sys
import logging
from .svc import CeidgService

log = logging.getLogger(__name__)

if __name__ == "__main__":
    try:
        cei = CeidgService()
        args = sys.argv[1:]
        if "--dump" in args:
            numpages = None
            if "--num" in args:
                numpages = int(args[2])
            cei.prepare_dump(numpages, clear=False)
    except KeyboardInterrupt:
        log.info("interrupted by the user. exiting.")
        sys.exit(1)
