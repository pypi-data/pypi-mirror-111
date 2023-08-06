from dataclasses import dataclass


@dataclass
class Durations:
    work_mins: int = 25
    break_mins: int = 5
    total_mins: int = 0


welcome_choices = (
    "",
    "q",
)

