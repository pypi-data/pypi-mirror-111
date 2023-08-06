from colorama import Fore, Style
import sys
import logging
from sylo.models import Durations
from pyfiglet import figlet_format
logger = logging.getLogger(__name__)


def print_message(message: str, timer_val: int = None):
    logger.debug(f'Printing message: {message} with a timer_val of {timer_val}')
    if message == "work_start":
        print(f"{Fore.RED}WORK{Style.RESET_ALL} for {Fore.YELLOW}{timer_val}{Style.RESET_ALL} minutes")
    elif message == "rest_start":
        print(f"{Fore.GREEN}REST{Style.RESET_ALL} for {Fore.YELLOW}{timer_val}{Style.RESET_ALL} minutes")
    elif message == "summary_and_quit":
        sys.stdout.write("\033[K")
        print(
            f"{Fore.BLUE}Press ENTER to stop timer.{Style.RESET_ALL}",
        )


def options():
    return """Additional commands;
S       --    Swap upcoming timer
Q       --    Quit SYLO
"""


def print_update(durations: Durations, mode: str, show_options: bool = False):
    logger.debug(f'Printing update: {mode} with show_options {show_options}')
    if mode == 'rest':
        upcoming_timer_color = durations.rest.bar_color
    else:
        upcoming_timer_color = durations.work.bar_color

    if show_options:
        print_ops = options()
    else:
        print_ops = '.. or chose an optional command (H for help)'
    print(
        f"""
Work length:        {Fore.RED}{durations.work.mins} minutes{Style.RESET_ALL}
Rest length:        {Fore.GREEN}{durations.rest.mins} minutes{Style.RESET_ALL}
Total work time:    {Fore.YELLOW}{durations.total_mins} minutes{Style.RESET_ALL}
Upcoming timer:     {upcoming_timer_color}{mode.upper()}{Style.RESET_ALL}

{Fore.BLUE}Press {Style.RESET_ALL}{Fore.YELLOW}ENTER {Style.RESET_ALL}{Fore.BLUE}to start the next timer{Style.RESET_ALL}

{Fore.BLUE}{print_ops}{Style.RESET_ALL}
    """)


def ascii_header(font: str):
    return figlet_format('Sort Your Life Out', font=font, width=40)


def print_header_small(double: bool, font: str):
    if double is True:
        color = Fore.BLUE
        double_message = '>>>>>>>>>>>> DOUBLE SPEED MODE >>>>>>>>>>>>'
    else:
        color = Fore.RED
        double_message = ''
    print(f"{double_message}")
    print(f"""{color}{ascii_header_small(font)}{Style.RESET_ALL}""")


def ascii_header_small(font: str):
    return figlet_format('SYLO', font=font, width=60)
