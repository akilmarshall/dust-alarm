# Dust Alarm

The dust alarm is a gui program that monitors an API and warns a user when the particle count has exceed the tolerance.

 - The warning is audible (and eventually visual)
 - Monitors Keck's inner dome sensor

## Development plan

### Beta

Create a command line program that can be control by parameter that sounds an audible alarm when the particle count has exceed the tolerance.

parameters:

- particle tolerance

### Release

Create a gui program (tkinter) that audibly warns the user when the particle count has exceeded tolerance.

- particle tolerance can be controlled via the gui 
- the current particle count is displayed on the gui
- the user is visually warned though the gui

## TTS

[Text-to-Speech (TTS) with Tacotron2 trained on LJSpeech](https://huggingface.co/speechbrain/tts-tacotron2-ljspeech?text=The+particle+count+has+exceeded+fifty+particles+per+leeter+of+air). 

I used the web interface to generate flac files for the following phrases (incorrect spelling for proper pronunciation):

- The particle count has exceeded fifty particles per leeter of air
- The particle count has exceeded one hundred particles per leeter of air
- The particle count has exceeded one hundred and fifty particles per leeter of air
- The particle count has exceeded two hundred particles per leeter of air
- The particle count has exceeded two hundred and fifty particles per leeter of air
- The particle count has exceeded three hundred particles per leeter of air
- The particle count has exceeded three hundred and fifty particles per leeter of air
- The particle count has exceeded four hundred particles per leeter of air
- The particle count has exceeded four hundred and fifty particles per leeter of air
- The particle count has exceeded five hundred particles per leeter of air

The flac files were then convert to wav files using the following command:

```bash
flac -d <flac_file>
```

## Install

Create a file secret.py in the same directory as dust_alarm.py with the following two variables

```python
SOUND_FILES = 'absolute/path/to/sound/file/directory'
KECK_API = 'Keck particle api url'
```

Ensure the following aliases exists on the user account interested in using this software

```bash
alias dust_alarm="/jac_sw/itsroot/src/itsScripts/arc/general/dust-alarm/dust_alarm.py &"
alias dust_alarm_quiet="/jac_sw/itsroot/src/itsScripts/arc/general/dust-alarm/dust_alarm.py --quiet &"
```

## Usage

```bash
# normal usage
$ dust_alarm  # fg and end the process to end the alarm program or kill the whole terminal.
# quiet usage, no output to terminal
$ dust_alarm_quiet
```
