#!/local/python3/bin/python3
"""
Version: Beta

This program checks at an interval of 5 minutes the particle count in Keck's
inner dome against a threashold.
When the particle count exceeds this threshold an audio alarm is played.

WAM December 8 2022
"""
from argparse import ArgumentParser
from datetime import datetime
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


def sound_file(particles):
    """
    For a given particle count, return the path to the appropreate sound file.
    i.e. for a particle count of 201 return the path to the sound file 200.wav
    'the particle count has exceeded 200 particles per liter of air'

    """
    files = [int(f.stem) for f in SOUND_PATH.iterdir()]
    files = sorted(files)
    sound_file = ''
    for a, b in zip(files, files[1:]):
        if a < particles <= b:
            sound_file = SOUND_PATH / f'{a}.wav'
            break
    else:
        sound_file = SOUND_PATH / '500.wav'

    return sound_file


def particles():
    """
    Call and parse the Keck api and return the current paricle count
    """
    response = get(KECK_API)
    if response.ok:
        body = response.text.split('\n')
        return float(body[-1].split()[1])
    return 0


def play_sound(path):
    """
    Use paplay to play the wav file at <path>
    """
    system(f'paplay {path.absolute()}')


# print current tolerance
print(f'tolerance: {TOLERANCE}')


# call the API and attempt to sound an alarm
if args.simulate:
    p_3m = args.simulate
else:
    p_3m = particles()

if not args.quiet:
    now = datetime.now()
    print(f'particle count: {p_3m}\t{now.year}{now.month:02d}{now.day:02d} {now.hour}:{now.minute:02d}')

if p_3m > TOLERANCE:
    # play audio alarm
    play_sound(sound_file(p_3m))


# forever, sleep 5 minutes
# call the API and attempt to sound an alarm
while True:
    sleep(5 * 60)  # sleep for 5 minutes
    p_3m = particles()

    if not args.quiet:
        now = datetime.now()
        print(f'particle count: {p_3m}\t{now.year}{now.month:02d}{now.day:02d} {now.hour}:{now.minute:02d}')

    if p_3m > TOLERANCE:
        # play audio alarm
        play_sound(sound_file(p_3m))

