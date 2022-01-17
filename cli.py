from __future__ import annotations

from gooey import Gooey, GooeyParser

from plais.__main__ import main


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
    
    parser.add_argument('-r', '--send-report', default='user@domain.com', 
        type=str, help='email to send the report to [not implemented yet!]')

    main(parser.parse_args())


if __name__ == '__main__':
    gui_generator()
