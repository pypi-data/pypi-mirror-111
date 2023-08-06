import argparse


def get_arguments():
    parser = argparse.ArgumentParser(
        description="Sort Your Life Out! Python Pomodoro Timer"
    )
    parser.add_argument("-w", "--work_time", help="Set the work time length", type=int)
    parser.add_argument(
        "-r", "--rest_time", help="Set the rest time length", type=int
    )
    parser.add_argument("-d", '--double_speed', dest='double_speed', action='store_true')
    parser.set_defaults(double_speed=False)
    return parser.parse_args()
