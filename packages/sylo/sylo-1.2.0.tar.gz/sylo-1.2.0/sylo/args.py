import argparse


def get_arguments():
    parser = argparse.ArgumentParser(
        description="Sort Your Life Out! Python Pomodoro Timer"
    )
    parser.add_argument("-w", "--work_time", help="Set the work time length", type=int)
    parser.add_argument(
        "-b", "--break_time", help="Set the break time length", type=int
    )
    return parser.parse_args()
