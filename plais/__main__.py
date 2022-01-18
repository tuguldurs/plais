from __future__ import annotations

import logging

from tqdm import tqdm

from .recording import Recording
from .frame import MedianVoxel
from .residual import Residual

log  = logging.getLogger(__name__)
fmt = '%(asctime)s ~ %(name)14s ~ %(levelname)8s ::: %(message)s'
lvl = logging.INFO
logging.basicConfig(level=lvl, format=fmt)

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


#if __name__ == '__main__':
#    main(args)