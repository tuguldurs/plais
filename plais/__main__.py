from __future__ import annotations

import logging

from tqdm import tqdm

from .recording import Recording
from .frame import Frame, MedianVoxel

log  = logging.getLogger(__name__)
fmt = '%(asctime)s ~ %(name)14s ~ %(levelname)8s ::: %(message)s'
lvl = logging.INFO
logging.basicConfig(level=lvl, format=fmt)

__all__ = ['plais']


def main(args) -> None:
    # args.speed
    rec = Recording(args.FileChooser)
    median_filter = MedianVoxel(rec, 0, 180).filter

    log.info(f'analysis duration {args.start} - {args.end} [sec]')
    for i in tqdm(range(args.start, args.end)):
        idx = i * rec.fps
        idx_next = (i + 1) * rec.fps
        frame = Frame(rec.frame(idx)).crop
        frame_next = Frame(rec.frame(idx_next)).crop
        absdiff = abs(frame_next - frame)
        residual = median_filter - absdiff
        residual[residual > 0] = 0
        residual = abs(residual)


if __name__ == '__main__':
    main(args)