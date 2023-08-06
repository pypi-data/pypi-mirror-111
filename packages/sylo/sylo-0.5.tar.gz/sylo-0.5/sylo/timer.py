#!/usr/bin/env python
import argparse
import sys
import time
import os
import simpleaudio
from beepy import beep
from sylo.messages import print_message, print_welcome, print_update
from sylo.models import Durations, welcome_choices
from sylo.definitions import AUDIO_FILE_PATH


def get_first_file_in_directory(path: str):
    return path + os.listdir(path)[0]


def initialise_wav(file_path):
    try:
        return simpleaudio.WaveObject.from_wave_file(
            get_first_file_in_directory(file_path)
        )
    except IndexError:
        print(f"Can't find a valid file in {file_path}. Using stock sounds.")
        return 'beep'


def play_sound(sound_file: any, beep_sound: str = 'coin'):
    if sound_file == 'beep':
        beep(sound=beep_sound)
    else:
        beep(sound=beep_sound)
        play_obj = sound_file.play()
        play_obj.wait_done()


def flip_mins_and_secs(time_val: int, mins_to_secs: bool = True):
    if mins_to_secs:
        return int(time_val * 60)
    else:
        return int(time_val / 60)


def start_timer(timer_mins: int, mode: str):
    timer_secs = flip_mins_and_secs(timer_mins)
    while timer_secs > 0:
        if timer_secs % 60 == 0:
            print_message(f'{mode}_start', flip_mins_and_secs(timer_secs, False))
        if timer_secs < 60:
            print_message(f'{mode}_countdown', timer_secs)
        time.sleep(1)
        timer_secs -= 1
    print_message(f'{mode}_stop', flip_mins_and_secs(timer_secs, False))


def sylo(is_break: bool, durations: Durations, sound_obj: any):
    print_update(durations)
    response = input('> ')
    os.system('cls' if os.name == 'nt' else 'clear')

    while response.lower() not in welcome_choices:
        print_welcome()
        sylo(is_break, durations)
    while response.lower() == "q":
        sys.exit()
    while response == "":
        if is_break:
            start_timer(durations.break_mins, 'break')
            play_sound(sound_obj, 'ready')
            is_break = False
        else:
            start_timer(durations.work_mins, 'work')
            play_sound(sound_obj, 'success')
            durations.total_mins += durations.work_mins
            is_break = True
        sylo(is_break, durations, sound_obj)


def run(args):
    print_welcome()
    wave_obj = initialise_wav(AUDIO_FILE_PATH)
    play_sound(wave_obj, 'coin')
    break_time = False
    durations_data = Durations()

    if args.work_time:
        durations_data.work_mins = args.work_time
    if args.break_time:
        durations_data.break_mins = args.break_time
    sylo(break_time, durations_data, wave_obj)


