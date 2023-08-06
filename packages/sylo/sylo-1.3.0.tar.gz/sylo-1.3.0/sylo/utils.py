import os


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def mins_to_secs(minutes: int):
    return minutes * 60


def flip_mode(mode: str):
    if mode == 'work':
        return 'rest'
    else:
        return 'work'
