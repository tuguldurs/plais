from __future__ import annotations

import logging

from PIL import Image
from PIL import ImageDraw

from .parse_config import parse_config
from . import package_output_path


log = logging.getLogger(__name__)


class Visuals:
	"""Generates graphics based on detections."""

	def __init__(self, video: recording.Recording, 
		               detections: detect.Detections) -> None:
		self.video = video
		self.detections = detections
		self.crop = parse_config('crop')
		self.outline_color = 'red'
		self.outline_width = 10

	@staticmethod
	def _get_bbox_size(imgsize, frameshape) -> tuple:
		"""Computes zoomed image size by retaining bbox aspect ratio."""
		framex, framey = frameshape[::-1]
		imgx, imgy = imgsize
		if imgx > imgy:
			size = framex, imgx * (framex // imgx)
		else:
			size = imgx * (framey // imgy), framey
		return size

	def _plot_zoom(self, i: int, frame: np.ndarray, bbox: tuple) -> None:
		"""Plots single detection with bounding box zoomer and contrasted."""
		savename = f'{package_output_path}/detection_zoom_{i:03}.png'
		img = Image.fromarray(frame)
		img = img.crop(self._get_bbox_patch(bbox))
		size = self._get_bbox_size(img.size, frame.shape[:-1])
		img = img.resize(size, Image.ANTIALIAS)
		img.save(savename)
		log.info(f'zoomed plot created for detection # {i}')
		log.info(f'plot saved in {savename}')

	def _get_bbox_patch(self, bbox: tuple) -> list:
		"""Create bounding box patch for PIL."""
		xmin, xmax, ymin, ymax = bbox
		xmin += self.crop['xmin']
		ymin += self.crop['ymin']
		xmax += self.crop['xmin']
		ymax += self.crop['ymin']
		return [xmin, ymin, xmax, ymax]

	def _plot_highlight(self, i: int, frame: np.ndarray, bbox: tuple) -> None:
		"""Plots single detection with bounding box highlighted."""
		savename = f'{package_output_path}/detection_{i:03}.png'
		img = Image.fromarray(frame)
		draw = ImageDraw.Draw(img)
		patch = self._get_bbox_patch(bbox)
		draw.rectangle(patch, outline=self.outline_color, width=self.outline_width)
		img.save(savename)
		log.info(f'highlighted plot created for detection # {i}')
		log.info(f'plot saved in {savename}')

	def _create_plots(self) -> None:
		"""Creates plots for all detections."""
		for i, idx in enumerate(self.detections.middle_idxs):
			idxsec, _, bbox, _ = self.detections.raw_record[idx]
			frame = self.video.frame(idxsec * self.video.fps)
			self._plot_highlight(i, frame, bbox)
			self._plot_zoom(i, frame, bbox)

	def generate(self):
		self._create_plots()
		#self._create_gifs()