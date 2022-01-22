from __future__ import annotations

import logging.config

from tqdm import tqdm
from numpy import arange as nparange

from utils.parse_config import parse_config
from .recording import Recording
from .frame import MedianVoxel
from .residual import Residual


logging.config.dictConfig(parse_config('logger'))
log = logging.getLogger(__name__)


__all__ = ['plais']



def main(args) -> None:
    # args.speed
    rec = Recording(args.FileChooser)
    if not args.end:
        args.end = int(rec.duration) - 1
    median_filter = MedianVoxel(rec, 0, 10).filter

    sec_multiplier = 2
    log.info(f'analysis duration {args.start} - {args.end} [sec]')
    log.info(f'frame fetch rate - every {sec_multiplier} second')
    n_steps = (args.end - args.start) // sec_multiplier
    idxs = nparange(n_steps) * sec_multiplier + args.start

    for i, idx in tqdm(enumerate(idxs)):
        if i == len(idxs) - 1:
            break
        frame = rec.frame(idx)
        frame_next = rec.frame(idxs[i+1])
        residual = Residual(frame, frame_next, median_filter, args.sensitivity)

        if residual.signal > 1000:
            issue = True
        else:
            issue = False
