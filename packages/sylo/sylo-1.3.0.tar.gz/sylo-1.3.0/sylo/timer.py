#!/usr/bin/env python
import sys
import time
import simpleaudio
from beepy import beep
from tqdm import tqdm
from colorama import Fore
from sylo.messages import (
    print_message,
    print_update,
    print_header_small,
)
from sylo.models import Durations
from sylo.definitions import (
    WELCOME_CHOICES,
    COUNTDOWN_INCREMENTS,
)
from sylo.utils import (
    clear_screen,
    mins_to_secs,
    flip_mode,
)


is_double = False
timer_mode = 'work'


class Timer:
    def __init__(self, mode: str, durations: Durations, increments: int):
        self.durations = durations
        self.mode: str = mode
        self.increments = increments

        if self.mode == "work":
            self.mins = self.durations.work.mins
            self.secs = self.durations.work.secs
            self.bar_color = self.durations.work.bar_color
        else:
            self.mins = self.durations.rest.mins
            self.secs = self.durations.rest.secs
            self.bar_color = self.durations.rest.bar_color

    def start_timer(self):
        timer_iterator = tqdm(
            total=self.secs,
            position=0,
            leave=True,
            desc=print_message(f'{self.mode}_start', self.mins),
            unit=" seconds",
            bar_format="{l_bar}%s{bar}%s{r_bar}" % (self.bar_color, Fore.RESET),
            smoothing=True,
            ncols=70
        )

        while self.secs > 0:
            time.sleep(1)
            self.secs -= self.increments
            timer_iterator.update(self.increments)
        timer_iterator.close()

    def start_countdown(self):
        self.start_timer()


class Sound:

    def __init__(self, audio_path: str = 'dummy'):
        self.sound_file = audio_path
        self.beep_needed = False
        self.initialised_file = None

    def initialise(self):
        try:
            self.initialised_file = simpleaudio.WaveObject.from_wave_file(
                self.sound_file
            )
        except FileNotFoundError:
            self.beep_needed = True

    def play_sound(self):
        if self.beep_needed is False:
            play_obj = self.initialised_file.play()
            play_obj.wait_done()
        else:
            beep("ready")


def sylo(
        durations_model: Durations,
        sound_obj: any,
        mode: str,
        show_options: bool,
        double: bool = is_double,
):
    clear_screen()

    if double is True:
        increments = 30
    else:
        increments = COUNTDOWN_INCREMENTS

    timer = Timer(mode, durations_model, increments)
    print_header_small(double=is_double, font='bubble')

    print_update(timer.durations, mode, show_options)

    response = input("> ")

    while response.lower() not in WELCOME_CHOICES:
        show_options = True
        sylo(
            durations_model=durations_model,
            sound_obj=sound_obj,
            mode=mode,
            show_options=show_options,
            double=double,
        )
    while response.lower() == "q":
        clear_screen()
        sys.exit()
    while response.lower() == "s":
        new_mode = flip_mode(mode)
        sylo(
            durations_model=durations_model,
            sound_obj=sound_obj,
            mode=new_mode,
            show_options=show_options,
            double=double,
        )
    while response.lower() == "h":
        show_options = True
        sylo(durations_model=durations_model,
             sound_obj=sound_obj,
             mode=mode,
             show_options=show_options,
             double=double,
             )
    clear_screen()
    while response == "":
        if mode == 'rest':
            timer.start_countdown()
            sound_obj.play_sound()
            mode = 'work'
        else:
            timer.start_countdown()
            sound_obj.play_sound()
            durations_model.total_mins += durations_model.work.mins
            mode = 'rest'
        sylo(
            durations_model=durations_model,
            sound_obj=sound_obj,
            mode=mode,
            show_options=False,
            double=double,
        )


def run(args):
    global is_double, timer_mode
    clear_screen()

    durations_data = Durations()

    if args.work_time:
        durations_data.work.mins = args.work_time
        durations_data.work.secs = mins_to_secs(args.work_time)
    if args.rest_time:
        durations_data.rest.mins = args.rest_time
        durations_data.rest.secs = mins_to_secs(args.rest_time)
    if args.double_speed is True:
        is_double = True
    if args.audio_file:
        sound = Sound(audio_path=args.audio_file)
    else:
        sound = Sound()
    print(args.audio_file)
    sound.initialise()

    sylo(
        durations_model=durations_data,
        sound_obj=sound,
        mode=timer_mode,
        show_options=False,
        double=is_double,
    )
