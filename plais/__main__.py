from __future__ import annotations

import logging.config

from tqdm import tqdm

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
    median_filter = MedianVoxel(rec, 0, 180).filter

    sec_multiplier = 2
    log.info(f'analysis duration {args.start} - {args.end} [sec]')
    log.info(f'frame fetch rate - every {sec_multiplier} second')
    Nsteps = (args.end - args.start) // sec_multiplier

    for i in tqdm(range(Nsteps)):
        tsec = args.start + i * sec_multiplier
        idx_current = tsec * rec.fps
        idx_next = (tsec + sec_multiplier) * rec.fps
        current_frame = rec.frame(idx_current)
        next_frame = rec.frame(idx_next)
        residual = Residual(current_frame, next_frame, median_filter, args.sensitivity)

        if residual.signal > 1000:
            issue = True
        else:
            issue = False

