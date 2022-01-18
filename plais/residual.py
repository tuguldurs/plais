from __future__ import annotations

import logging

import numpy as np
from skimage.filters import gaussian

from .frame import Frame


log = logging.getLogger(__name__)


class Residual:
	"""Difference imaging with respect to median filter.

	Attributes:
		current_frame - Raw grayscale frame at current index.
		next_frame - Raw grayscale frame at next iteration index.
		median_filter - Median voxel filter image.
		sensitivity - Signal detector sensitivity.
	"""

	def __init__(self, current_frame: np.ndarray, 
		               next_frame: np.ndarray,
		               median_filter: np.ndarray, 
		               sensitivity: float) -> None:
		self.current = Frame(current_frame).processed
		self.next = Frame(next_frame).processed
		self.sensitivity = sensitivity
		self.image = self._residual_image(median_filter)
		self.signal = self._residual_signal()
		self.map = self._binary_gaussian()

	def _absdiff(self) -> np.ndarray:
		"""Computes absolute difference between current and next frames."""
		return abs(self.next - self.current)

	def _residual_image(self, median_filter: np.ndarray) -> np.ndarray:
		"""Computes residual image."""
		residual = median_filter * self.sensitivity - self._absdiff()
		residual[residual > 0] = 0
		return abs(residual)

	def _binary_gaussian(self) -> np.ndarray:
		"""Computes binary gaussian filter."""
		gaussian_filter = gaussian(self.image, sigma=3)
		gaussian_filter[gaussian_filter > 0] = 1
		return gaussian_filter

	def _residual_signal(self) -> int:
		"""Quantifies residual signal count by number of pixels."""
		gaussian_filter = self._binary_gaussian()
		return np.sum(gaussian_filter == 1)
