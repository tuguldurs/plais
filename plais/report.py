from __future__ import annotations

import logging

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

    def summary_page_body(self):
        ...

    def detection_page_body(self, images):
        """Prints body page."""
        self.image(images[0], 15, 50, self.width - 30)
        img = Image.open(images[1])
        x, y = img.size
        width_2nd_image = x * (self.height - 175) / y
        self.image(images[1], 15, 160, width_2nd_image)

    def print_summary_page(self):
        """Prints summary page."""
        #self.add_page()
        #self.summary_page_body()

    def print_detection_page(self, images):
        """Prints detection pages."""
        self.add_page()
        self.detection_page_body(images)


class Report:
    """Generates final pdf report document."""

    def __init__(self, detections) -> None:
        ...

    def generate(self) -> None:
        pdf = PDF()
        plots_per_page = [['PLAIS_RESULTS/detection_000.png','PLAIS_RESULTS/detection_zoom_000.png'],
                  ['PLAIS_RESULTS/detection_001.png','PLAIS_RESULTS/detection_zoom_001.png']]
        #pdf.print_summary_page(xxx)
        for elem in plots_per_page:
            pdf.print_detection_page(elem)
        pdf.output(f'{package_output_path}/report.pdf', 'F')