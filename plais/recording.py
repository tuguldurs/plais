from __future__ import annotations

import os
import logging
import datetime

import imageio
import numpy as np


log = logging.getLogger(__name__)


class Recording:
    """Reads input recording and extracts individual frames.

    Attributes:
        fname - full path to recording.
        speed - optional line speed [ft / min], defaults to 40.
        tinterval - optional start and end times for analysis [sec],
                    defaults to full interval.
    """
    
    def __init__(self, fname: str,
                 speed: float = 40,
                 tinterval: tuple = None) -> None:
        self.fname = fname
        self.video = imageio.get_reader(self.fname, 'ffmpeg')
        self.meta = self._get_meta_data()
        self.duration = self.meta['duration']
        self.fps = int(self.meta['fps'])
        self.size = self.meta['size']
        self.maxidx = self._get_index_length()
        self.logger()
        self.speed = speed
        if not tinterval:
            self.tstart = 0
            self.tend = self.duration

    def _get_meta_data(self) -> dict:
        """Fetches video meta-data."""
        return self.video.get_meta_data()

    def _get_index_length(self) -> int:
        """Computes maximum frame index."""
        return round(self.duration * self.fps)

    @staticmethod
    def rgb2gray(rgbimg: np.ndarray) -> np.ndarray:
        """Converts 3D rgb image into 2D grayscale."""
        return np.dot(rgbimg[..., :3], [0.299, 0.587, 0.114])

    def frame(self, idx: int, gray: bool = True) -> np.ndarray:
        """Fetches frame by index.

        Args:
            idx - Index of frame.
            gray - Optional flag for grayscale conversion.

        Returns:
            2D grayscale image if gray is True, 3D color image if gray is False.
        """
        frame = self.video.get_data(idx)
        if gray:
            return self.rgb2gray(frame)
        else:
            return frame

    def logger(self) -> None:
        """Logs input video info."""
        log.info('reading input video:')
        log.info(f'{self.fname}')
        log.info(f'video duration = {self.duration} seconds.')
        log.info(f'frame rate = {self.fps} per second.')
        log.info(f'frame size = {self.size}.')
