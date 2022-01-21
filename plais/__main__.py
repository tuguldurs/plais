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

    log.info(f'analysis duration {args.start} - {args.end} [sec]')
    for i in tqdm(range(args.start, args.end)):
        current_frame = rec.frame(i * rec.fps)
        next_frame = rec.frame((i + 1) * rec.fps)
        residual = Residual(current_frame, next_frame, median_filter, args.sensitivity)
        if residual.signal > 1000:
            issue = True
        else:
            issue = False
