from __future__ import annotations

import logging

import numpy as np
from tqdm import tqdm

from .parse_config import parse_config


log = logging.getLogger(__name__)


class Frame:
	"""Process raw RGB frame.

	Attributes:
		frame - RGB 3D image array.
		processed - Processed (cropped, patched) grayscale 2D image.
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
		"""Applies null patches to 2D grayscale image."""
		cropped = self.gray2crop(self.gray)
		patches = parse_config('patch')
		for patch in patches:
			grayimg = self.apply_patch(cropped, patch)
		return grayimg


class MedianVoxel:
	"""Creates median voxel filter.

	Attributes:
		frames - List of processed frames to build the filter.
		filter - Ready to use filter.
	"""

	def __init__(self, frames: list) -> None:
		self.frames = frames
		self.filter = self._get_filter()

	def _stack_frames(self) -> np.ndarray:
		"""Stacks collected frames."""
		return np.stack(self.frames, axis=-1)

	def _get_filter(self) -> np.ndarray:
		"""Computes median voxel filter based on standard deviation for each pixel."""
		stacked_frames = self._stack_frames()
		return np.std(stacked_frames, axis=-1)
