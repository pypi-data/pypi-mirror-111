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
            expand = '--expand' in args
            clear='--clear' in args
            if "--num" in args:
                numpages = int(args[2])
            cei.prepare_dump(numpages, expand=expand, clear=clear)
    except KeyboardInterrupt:
        log.info("interrupted by the user. exiting.")
        sys.exit(1)
