from __future__ import annotations

import logging

import numpy as np
from tqdm import tqdm

from .recording import Recording


log = logging.getLogger(__name__)


class Frame:
	"""Process raw RGB frame.

	Attributes:
		frame - RGB 3D image array.
	"""

	def __init__(self, frame) -> None:
		self.gray = self.rgb2gray(frame)
		self.processed = self.process(self.gray)

	@staticmethod
	def rgb2gray(rgbimg: np.ndarray) -> np.ndarray:
		"""Converts 3D rgb image into 2D grayscale."""
		return np.dot(rgbimg[..., :3], [0.299, 0.587, 0.114])

	@staticmethod
	def gray2crop(grayimg: np.ndarray) -> np.ndarray:
		"""Crops 2D grayscale image.

		TODO: this should be read from config file.
		"""
		return grayimg[400:900, 240:1640]

	@staticmethod
	def apply_patch(grayimg: np.ndarray, patch: list) -> np.ndarray:
		"""Applies null patches to 2D grayscale image."""
		grayimg[patch[0]:patch[1], patch[2]: patch[3]] = 0
		return grayimg


	def process(self, grayimg: np.ndarray) -> np.ndarray:
		"""Applies null patches to 2D grayscale image.

		TODO: patches should be read from config file.
		"""
		cropped = self.gray2crop(self.gray)
		patches = [[0,300,0,35], [0,270,0,60], [0,230,0,85], [0,180,0,100], 
		           [0,300,1360,1400], [0,240,1330,1360], [0,200,1300,1330], [0,150,1280,1300]]
		for patch in patches:
			grayimg = self.apply_patch(cropped, patch)
		return grayimg


class MedianVoxel:
	"""Creates median voxel filter.

	Attributes:
		rec - Input video as Recording object.
		tstart - Time to start extracting frames.
		tend - Time to end extracting frames.
	"""

	def __init__(self, rec: Recording, tstart: int, tend: int) -> None:
		self.rec = rec
		self.tstart = tstart
		self.tend = tend
		self.idxs = self._idx_second()
		self.filter = self._get_filter()

	def _idx_second(self) -> np.ndarray:
		"""Computes idx array for every second of given duration."""
		duration = self.tend - self.tstart
		return np.arange(duration) * self.rec.fps

	def _collect_frames(self) -> list:
		"""Collects all frames by index."""
		return [Frame(self.rec.frame(idx)).processed for idx in tqdm(self.idxs)]

	def _stack_frames(self) -> np.ndarray:
		"""Stacks collected frames."""
		frames = self._collect_frames()
		return np.stack(frames, axis=-1)

	def _get_filter(self) -> np.ndarray:
		"""Computes median voxel filter based on standard deviation for each pixel."""
		log.info('creating filter...')
		stacked_frames = self._stack_frames()
		return np.std(stacked_frames, axis=-1)