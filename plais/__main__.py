from __future__ import annotations

import logging.config

from .recording import Recording


__all__ = ['plais']


def main(args) -> None:
    rec = Recording(args.FileChooser, args.start, args.end, args.speed)


if __name__ == '__main__':
    main(args)