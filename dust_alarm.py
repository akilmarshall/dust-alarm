#!/local/python3/bin/python3
"""
Version: Alpha

This program checks at an interval of 5 minutes the particle count in Keck's inner dome against a threashold.
When the particle count exceeds this threshold an audio alarm is played.

WAM December 8 2022
"""
from argparse import ArgumentParser
from os import system
from pathlib import Path
from time import sleep

from requests import get

from secret import KECK_API, SOUND_FILES


TOLERANCE = 250 
SOUND_PATH = Path(SOUND_FILES)

parser = ArgumentParser(description=__doc__)
parser.add_argument('--tolerance', '-t', type=float, default=TOLERANCE, help=f'define the partice tolerance ceiling. default: {TOLERANCE}')
parser.add_argument('--quiet', '-q', action='store_true', default=False, help='when passed nothing is output to stdout') 
parser.add_argument('--simulate', '-s', type=float, help='set the paticle value for the first particle check. intended for testing purposes')

args = parser.parse_args()

TOLERANCE = args.tolerance

def sound_file(particles, most=500):
    """
    most is equal to the audio file for the largest amount of particles audio warnings are issued for.
    if new files are created update most accordingly
    """
    intervals = [(i, i + 50) for i in range(50, most, 50)]
    for (a, b) in intervals:
        if a < particles <= b:
            return SOUND_PATH / f'{a}.wav'
    if particles > most:
        return SOUND_PATH / f'{most}.wav'

def particles():
    response = get(KECK_API)
    if response.ok:
        body = response.text.split('\n')
        return float(body[-1].split()[1])
    return 0

def play_sound(path):
    system(f'paplay {path.absolute()}')


if args.simulate:
    p_3m = args.simulate
else:
    p_3m = particles()

if p_3m > TOLERANCE:
    # play audio alarm
    play_sound(sound_file(p_3m))

if not args.quiet:
    print(f'particle count: {p_3m}')

while True:
    sleep(5 * 60)  # sleep for 5 minutes
    p_3m = particles()
    if p_3m > TOLERANCE:
        # play audio alarm
        play_sound(sound_file(p_3m))

    if not args.quiet:
        print(f'particle count: {p_3m}')
