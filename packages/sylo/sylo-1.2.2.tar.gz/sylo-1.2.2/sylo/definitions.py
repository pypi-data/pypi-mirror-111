import os


ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

AUDIO_FILE_PATH = f"{ROOT_DIR}/audio/"

WELCOME_CHOICES = (
    "",
    "q",
    "s",
)

TIMER_DEFAULTS = {
    "work": {
        "mins": 25,
        "secs": 1500,
    },
    "rest": {
        "mins": 5,
        "secs": 300,
    }
}

COUNTDOWN_INCREMENTS = 1
