from __future__ import annotations

import logging.config

from .recording import Recording


__all__ = ['plais']


class Plais:
    """..."""

    def __init__(self):
        ...

    def run(self, fname: str) -> None:
        rec = Recording(fname)
