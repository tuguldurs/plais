from __future__ import annotations

import logging

import numpy as np


log = logging.getLogger(__name__)


class Frame:
	"""Process raw RGB frame.

	Attributes:
		frame - RGB 3D image array.
	"""

	def __init__(self, frame) -> None:
		self.gray = self.rgb2gray(frame)
		self.crop = self.gray2crop(self.gray)

	@staticmethod
	def rgb2gray(rgbimg: np.ndarray) -> np.ndarray:
		"""Converts 3D rgb image into 2D grayscale."""
		return np.dot(rgbimg[..., :3], [0.299, 0.587, 0.114])

	@staticmethod
	def gray2crop(grayimg: np.ndarray) -> np.ndarray:
		"""Crops 2D grayscale image.

		TODO: this should be read from config file, possibly 
		      controlled by the choice arg.
		"""
		return grayimg[400:1000, 240:1640]
