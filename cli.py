from gooey import Gooey, GooeyParser

from plais import main


@Gooey(dump_build_config=True, program_name="PLAIS")
def gui_generator():
    desc = "Steel Line Video Analyzer for Wolverine"
    file_help_msg = "Click on Browse and select the video file you want to process"

    parser = GooeyParser(description=desc)

    parser.add_argument("FileChooser", help=file_help_msg, widget="FileChooser")
    
    parser.add_argument('--start-time', 
        help='in video datetime where processing should begin', widget="TimeChooser")
    parser.add_argument('--end-time', 
        help='in video datetime where processing should end', widget="TimeChooser")

    parser.add_argument('-d', '--send-report', default='pizda@pizda.com', 
        type=str, help='email to send the report to [not implemented yet!]')

    args = parser.parse_args()

    print(args.FileChooser)


if __name__ == '__main__':
    gui_generator()
