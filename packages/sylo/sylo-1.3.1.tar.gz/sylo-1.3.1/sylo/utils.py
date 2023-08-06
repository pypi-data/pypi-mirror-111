import os
import logging


logger = logging.getLogger(__name__)


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def mins_to_secs(minutes: int):
    return minutes * 60


def flip_mode(mode: str):
    if mode == 'work':
        logger.debug(f'flip_mode took {mode} returned rest')
        return 'rest'
    else:
        logger.debug(f'flip_mode took {mode} returned work')
        return 'work'
