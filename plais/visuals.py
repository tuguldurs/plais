from __future__ import annotations

import logging
import matplotlib.pyplot as plt


log = logging.getLogger(__name__)


class Visuals:
	"""Generate graphics based on detections."""

	def __init__(self, detections) -> None:
		self.detections = detections

	def _draw_bbox(ax, bbox) -> axes.Axes:
		...

	def _plot_scrnshot(idx) -> axes.Axes:
		...

	def _plot_detections():
		...