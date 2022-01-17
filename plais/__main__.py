from __future__ import annotations

import logging.config

from .recording import Recording


__all__ = ['plais']


def main(args) -> None:
    print(args)
    print(vars(args))
    rec = Recording(args.FileChooser, 0, 10)


if __name__ == '__main__':
    main(args)