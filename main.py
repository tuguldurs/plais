from __future__ import annotations

import logging.config

from tqdm import tqdm
from numpy import arange as nparange
from multiprocessing import Pool, cpu_count, freeze_support
from gooey import Gooey, GooeyParser
from imageio import get_reader

from plais.parse_config import parse_config
from plais.recording import Recording
from plais.frame import Frame, MedianVoxel
from plais.residual import Residual


logging.config.dictConfig(parse_config('logger'))
log = logging.getLogger(__name__)


@Gooey(dump_build_config=True, program_name="PLAIS")
def gui_generator() -> None:
    """Generate minimal GUI and call main with args."""

    desc = "Steel Line Video Analyzer for Wolverine"
    help_msg = "Click on Browse and select the video file you want to process"

    parser = GooeyParser(description=desc)

    parser.add_argument("FileChooser", help=help_msg, widget="FileChooser")
    
    parser.add_argument('-b', '--start', default=0,
        type=int, help='start time [seconds])')

    parser.add_argument('-e', '--end',
        type=int, help='end time [seconds]')

    parser.add_argument('-s', '--speed', default=40,
        type=int, help='line speed [feet / minute]')

    parser.add_argument('-x', '--sensitivity', default=10,
        type=float, help='detector sensitivity [smaller more sensitive]')
    
    parser.add_argument('-r', '--send-report', default='user@domain.com', 
        type=str, help='email to send the report to [not implemented yet!]')

    args = parser.parse_args()

    plais = Plais(args)
    plais.run()


##########################################################################################

class Args:
    def __init__(self, fname, tstart, tend, speed, sensitivity):
        self.FileChooser = fname
        self.start = tstart
        self.end = tend
        self.speed = speed
        self.sensitivity = sensitivity

def tst():
    fname = 'd/steel_line_test.mp4'
    args = Args(fname, 1150, 1160, 40, 10)
    p = Plais(args)
    p.run()

##########################################################################################


class Plais:
    """Prod-Line ai system for Wolverine."""
    
    def __init__(self, args):
        self.fname = args.FileChooser
        self.tstart = args.start
        self.tend = args.end
        self.sensitivity = args.sensitivity
        self.n_cpu = cpu_count() - 2

    @staticmethod
    def _process_frame(idx, fname) -> np.ndarray:
        """Process raw rgb frame through Frame."""
        with get_reader(fname, 'ffmpeg') as reader:
            frame = reader.get_data(idx)
        return Frame(frame).processed

    def _collect_frames(self, rec) -> list:
        """Collects processed frames for median filter.

        TODO: this is a terrible parallelization, need shared memory for rec object.
        """
        rec = Recording(self.fname)
        with Pool(self.n_cpu) as pool:
            log.info(f'collecting frames for filter with {self.n_cpu} workers...')
            results = [pool.apply_async(self._process_frame, (idx * rec.fps, self.fname)) for idx in range(100)]
            frames = [result.get() for result in tqdm(results)]
        return frames

    def run(self):
        rec = Recording(self.fname)
        if not self.tend:
            self.tend = int(rec.duration) - 2
        frames = self._collect_frames(rec)
        median_filter = MedianVoxel(frames).filter
        log.info('filter created.')

        sec_multiplier = 2
        log.info(f'analysis duration {self.tstart} - {self.tend} [sec]')
        log.info(f'frame fetch rate - every {sec_multiplier} second')
        n_steps = (self.tend - self.tstart) // sec_multiplier
        idxs = nparange(n_steps) * sec_multiplier + self.tstart

        for i, idx in tqdm(enumerate(idxs)):
            if i == len(idxs) - 1:
                break
            frame = rec.frame(idx)
            frame_next = rec.frame(idxs[i+1])
            residual = Residual(frame, frame_next, median_filter, self.sensitivity)

            if residual.signal > 1000:
                issue = True
            else:
                issue = False

            print(idx, issue, residual.signal)


if __name__ == '__main__':
    freeze_support()
    gui_generator()
    #tst()
