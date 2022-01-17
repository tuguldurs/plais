from __future__ import annotations

import logging

from imageio import get_reader
import numpy as np


log = logging.getLogger(__name__)


class Recording:
    """Reads input recording and extracts individual frames.

    Attributes:
        fname - Full system path to recording file.
    """
    
    def __init__(self, fname: str) -> None:
        self.fname = fname
        self.video = get_reader(self.fname, 'ffmpeg')
        self.meta = self._get_meta_data()
        self.duration = self.meta['duration']
        self.fps = int(self.meta['fps'])
        self.size = self.meta['size']
        self.maxidx = self._get_index_length()
        self.logger()

    def _get_meta_data(self) -> dict:
        """Fetches video meta-data."""
        return self.video.get_meta_data()

    def _get_index_length(self) -> int:
        """Computes maximum frame index."""
        return round(self.duration * self.fps)

    def frame(self, idx: int) -> np.ndarray:
        """Fetches frame by index.

        Args:
            idx - Index of frame.

        Returns:
            3D color image.
        """
        return self.video.get_data(idx)

    def logger(self) -> None:
        """Logs input video info."""
        log.info('reading input video:')
        log.info(f'{self.fname}')
        log.info(f'video duration = {self.duration} seconds.')
        log.info(f'frame rate = {self.fps} per second.')
        log.info(f'frame size = {self.size}.')
