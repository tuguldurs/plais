from __future__ import annotations

import logging

from PIL import Image
from PIL import ImageDraw


log = logging.getLogger(__name__)


class Visuals:
	"""Generate graphics based on detections."""

	def __init__(self, video: recording.Recording, 
		               detections: detect.Detections, 
		               outdir: str) -> None:
		self.video = video
		self.detections = detections
		self.outdir = outdir
		self.outline_color = 'red'
		self.outline_width = 10

	def _plot_zoom():
		...

	@staticmethod
	def _get_bbox_patch(bbox: tuple) -> bbox_patch:
		"""Create bounding box patch for PIL."""
		xmin, xmax, ymin, ymax = bbox
		return [xmin, ymin, xmax, ymax]

	def _plot_highlight(self, i: int, frame: np.ndarray, bbox: tuple) -> None:
		"""Plots single detection with bounding box highlighted."""
		savename = f'{self.outdir}/detection_{i:03}.png'
		img = Image.fromarray(frame)
		draw = ImageDraw.Draw(img)
		patch = self._get_bbox_patch(bbox)
		draw.rectangle(patch, outline=self.outline_color, width=self.outline_width)
		img.save(savename)
		log.info(f'highlighted plot created for detection # {i}')
		log.info(f'plot saved in {savename}')

	def _plot_detections(self) -> None:
		"""."""
		for i, idx in enumerate(self.detections.middle_idxs):
			idxsec, _, bbox, _, _ = self.detections.raw_record[idx]
			frame = self.video.frame(idxsec * self.video.fps)
			self._plot_highlight(i, frame, bbox)

	def generate(self):
		self._plot_detections()