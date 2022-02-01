from __future__ import annotations

import logging
from datetime import timedelta

from fpdf import FPDF
from PIL import Image
from . import package_output_path


log = logging.getLogger(__name__)


class PDF(FPDF):
    """Inherited class from fpdf for general config and methods."""
    def __init__(self):
        super().__init__()
        self.width = 210
        self.height = 297
        self.breakheight = '20'
        
    def header(self):
        """Header config."""
        self.set_font('Arial', 'B', 11)
        self.cell(self.width - 80)
        self.cell(60, 1, 'Video Analysis Report by PLAIS', 0, 0, 'R')
        self.ln(20)
        
    def footer(self):
        """Footer config."""
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.set_text_color(128)
        self.cell(0, 10, 'Page ' + str(self.page_no()), 0, 0, 'C')

    def summary_page_body(self, rec, tstart, tend, ndetections):
        self.set_font('Arial', 'B', 15)
        self.cell(0, 1, 'Input File:', 0, 1)
        self.cell(0, 10, f'{rec.fname}', 0, 2, 'C')
        self.ln(h=self.breakheight)
        self.cell(0, 10, f'total duration: {rec.duration}', 0, 1)
        self.cell(0, 10, f'frame rate: {rec.fps}', 0, 1)
        self.cell(0, 10, f'frame size: {rec.size} pixels', 0, 2)
        self.ln(h=self.breakheight)
        self.cell(0, 10, f'analysis starts: {tstart} seconds ({timedelta(seconds=tstart)})', 0, 1)
        self.cell(0, 10, f'analysis ends: {tend} seconds ({timedelta(seconds=tend)})', 0, 1)
        self.cell(0, 10, f'analysis duration: {tend - tstart} seconds', 0, 2)
        self.ln(h=self.breakheight)
        if ndetections:
            self.set_text_color(255,0,0)
        self.cell(0, 10, f'number of unique problems identified: {ndetections}')

    def detection_page_body(self, i, info, images):
        """Prints body page."""
        tsec, length_m, length_ft = info
        self.set_text_color(0,0,0)
        self.set_font('Arial', 'B', 15)
        self.cell(0, 10, f'Detection # {i}:', 0, 1)
        self.set_font('Arial', '', 11)
        info_line = f'time: {tsec} seconds ({timedelta(seconds=float(tsec))})  |  '
        info_line += f'position: {length_m:.1f} [m] / {length_ft:.1f} [ft]'
        self.cell(0, 10, info_line)
        self.image(images[0], 15, 50, self.width - 30)
        img = Image.open(images[1])
        x, y = img.size
        width_zoom_image = x * (self.height - 175) / y
        self.image(images[1], 15, 160, width_zoom_image)

    def print_summary_page(self, rec, tstart, tend, ndetections):
        """Prints summary page."""
        self.add_page()
        self.summary_page_body(rec, tstart, tend, ndetections)

    def print_detection_page(self, i, info, images):
        """Prints detection pages."""
        self.add_page()
        self.detection_page_body(i, info, images)


class Report:
    """Generates final pdf report document."""

    def __init__(self, rec, tstart, tend, detections, speed) -> None:
        self.rec = rec
        self.tstart = tstart
        self.tend = tend
        self.detections = detections
        self.ndetections = len(detections.middle_idxs)
        self.speed = speed

    def _get_detection_info(self, idx) -> list:
        """Compile basic detection info to print."""
        tsec = self.detections.raw_record[idx][0]
        length_m = self.speed * (tsec / 60)
        length_ft = length_m / 0.3048
        return [tsec, length_m, length_ft]

    def generate(self) -> None:
        """Generates report page by page."""
        log.info('generating report...')
        pdf = PDF()
        pdf.print_summary_page(self.rec, self.tstart, self.tend, self.ndetections)
        for i, idx in enumerate(self.detections.middle_idxs):
            info = self._get_detection_info(idx)
            detection_plot = f'{package_output_path}/detection_{i:03}.png'
            zoom_plot = f'{package_output_path}/detection_zoom_{i:03}.png'
            pdf.print_detection_page(i+1, info, [detection_plot, zoom_plot])
        pdf.output(f'{package_output_path}/report.pdf', 'F')
        log.info(f'report generated in {package_output_path}/report.pdf')