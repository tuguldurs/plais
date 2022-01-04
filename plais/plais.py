from __future__ import annotations

import logging.config

from .recording import Recording


__all__ = ['plais']


def main(fname: str) -> None:
    rec = Recording(fname)
