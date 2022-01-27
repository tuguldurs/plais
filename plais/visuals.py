from __future__ import annotations

import logging

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch as bbox_patch



log = logging.getLogger(__name__)


class Visuals:
	"""Generate graphics based on detections."""

	def __init__(self, video: recording.Recording, 
		               detections: detect.Detections, 
		               outdir: str) -> None:
		self.video = video
		self.detections = detections
		self.outdir = outdir

	def _plot_zoom():
		...

	@staticmethod
	def _get_bbox_patch(bbox: tuple) -> bbox_patch:
		"""Draws bounding box."""
		xmin, xmax, ymin, ymax = bbox
		patch = bbox_patch((xmin, ymin), xmax-xmin, ymax-ymin,
			boxstyle='round, pad=0.1', fc='tomato', lw=3)
		return patch

	def _plot_highlight(self, i: int, frame: np.ndarray, bbox: tuple) -> None:
		"""Plots single detection with bounding box highlighted."""
		savename = f'{self.outdir}/detection_{i:03}.png'
		fig, ax = plt.subplots(tight_layout=True)
		#ax.axis('off')
		ax.imshow(frame)
		ax.add_patch(self._get_bbox_patch(bbox))
		plt.savefig(savename)
		log.info(f'highlighted plot created for detection # {i}')
		log.info(f'plot saved in {savename}')
		plt.close()

	def _plot_detections(self) -> None:
		"""."""
		for i, idx in enumerate(self.detections.middle_idxs):
			idxsec, _, bbox, _, _ = self.detections.raw_record[idx]
			frame = self.video.frame(idxsec * self.video.fps)
			self._plot_highlight(i, frame, bbox)

	def generate(self):
		self._plot_detections()