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
            expand = "--expand" in args
            clear = "--clear" in args
            if "--num" in args:
                num_page_val_idx = args.index("--num") + 1
                numpages = int(args[num_page_val_idx])
            cei.prepare_dump(numpages, expand=expand, clear=clear)
    except KeyboardInterrupt:
        log.info("interrupted by the user. exiting.")
    except IndexError as e:
        log.info(f"cannot handle input args. {str(e)}")
