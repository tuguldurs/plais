from __future__ import annotations

import logging

from .recording import Recording

log  = logging.getLogger(__name__)
fmt = '%(asctime)s ~ %(name)14s ~ %(levelname)8s ::: %(message)s'
lvl = logging.INFO
logging.basicConfig(level=lvl, format=fmt)

__all__ = ['plais']


def main(args) -> None:
    # args.start
    # args.end
    # args.speed
    rec = Recording(args.FileChooser)


if __name__ == '__main__':
    main(args)