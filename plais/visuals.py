from __future__ import annotations

import logging
import matplotlib.pyplot as plt


log = logging.getLogger(__name__)


class Visuals:
	"""Generate graphics based on detections."""

	def __init__(self, video: recording.Recording, 
		               detections: detect.Detections, 
		               outdir: str) -> None:
		self.video = video
		self.detections = detections
		self.outdir = outdir

	def _draw_bbox(ax, bbox) -> axes.Axes:
		...

	def _plot_scrnshot(idx) -> axes.Axes:
		...

	def _plot_detections(self) -> None:
		"""."""
		for i, idx in enumerate(self.detections.middle_idxs):
			idxsec, _, bbox, _, _ = self.detections.raw_record[idx]
			frame = self.video.frame(idxsec * self.video.fps)
			fig, ax = plt.subplots(tight_layout=True)
			plt.imshow(frame)
			plt.savefig(f'{self.outdir}/detection_{i:03}.png')

	def generate(self):
		self._plot_detections()