from __future__ import annotations

import logging
from itertools import groupby


log = logging.getLogger(__name__)


class Detection:
	"""Extracts valid detections from raw records."""

	def __init__(self, record) -> None:
		self.raw_record = record
		self.boundary_idxs = self._get_boundary_idxs()
		self.middle_idxs = self._get_middle_idxs()
		self._logger()

	def _get_flags(self):
		"""Fetch all flags from raw record."""
		return [flag for _, flag, _, _ in self.raw_record]

	def _get_boundary_idxs(self):
		"""Computes boundary record indices of individual detections."""
		idx, boundaries = 0, []
		for key, group in groupby(self._get_flags()):
			group = list(group)
			if key == 0 or len(group) == 1:
				idx += len(group)
			else:
				start = idx
				idx += len(group)
				end = idx
				boundaries.append((start, end))
		return boundaries

	def _get_middle_idxs(self):
		"""Computes mid record indices for each detection."""
		idxs = []
		boundaries = self._get_boundary_idxs()
		for start, end in boundaries:
			idxs.append(round((start + end)/2))
		return idxs

	def _logger(self):
		log.info(f'number of unique events identified = {len(self.boundary_idxs)}.')
