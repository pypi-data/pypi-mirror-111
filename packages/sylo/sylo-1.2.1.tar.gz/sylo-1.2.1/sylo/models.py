from dataclasses import dataclass
from colorama import Fore
from sylo.definitions import TIMER_DEFAULTS


@dataclass
class Rest:
    mins: int = TIMER_DEFAULTS["rest"]["mins"]
    secs: int = TIMER_DEFAULTS["rest"]["secs"]
    bar_color: str = Fore.GREEN


@dataclass
class Work:
    mins: int = TIMER_DEFAULTS["work"]["secs"]
    secs: int = TIMER_DEFAULTS["work"]["secs"]
    bar_color: str = Fore.RED


@dataclass
class Durations:
    work = Work
    rest = Rest
    total_mins: int = 0

    def __post_init__(self):
        self.work = Work()
        self.rest = Rest()
