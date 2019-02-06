# -*- coding: utf-8 -*-
"""
Created on Fri Nov 23 12:52:11 2018

@author: Jon
"""

# Imports
import numpy as np
import matplotlib.pyplot as plt
# matplotlib inline
import pretty_midi
import librosa
import librosa.display
import mir_eval
import mir_eval.display
import tables
import IPython.display
import os
import json
import time


# Utility functions for retrieving paths
def msd_id_to_dirs(msd_id):
    """Given an MSD ID, generate the path prefix.
    E.g. TRABCD12345678 -> A/B/C/TRABCD12345678"""
    return os.path.join(msd_id[2], msd_id[3], msd_id[4], msd_id)


def msd_id_to_mp3(msd_id):
    """Given an MSD ID, return the path to the corresponding mp3"""
    return os.path.join(DATA_PATH, 'msd', 'mp3',
                        msd_id_to_dirs(msd_id) + '.mp3')


# h5 removed from following bracket
def msd_id_to_h5(msd_id):
    """Given an MSD ID, return the path to the corresponding h5"""
    return os.path.join(RESULTS_PATH, 'lmd_matched_h5',
                        msd_id_to_dirs(msd_id) + '.h5')


def get_midi_path(msd_id, midi_md5, kind):
    """Given an MSD ID and MIDI MD5, return path to a MIDI file.
    kind should be one of 'matched' or 'aligned'. """
    return os.path.join(RESULTS_PATH, 'lmd_{}'.format(kind),
                        msd_id_to_dirs(msd_id), midi_md5 + '.mid')


# Local path constants
DATA_PATH = 'data'
RESULTS_PATH = 'C:/Users/jonpo/Uni/Year 4/Project' #'results'
# Path to the file match_scores.json distributed with the LMD
SCORE_FILE = os.path.join(RESULTS_PATH, 'match_scores.json')

with open(SCORE_FILE) as f:
    scores = json.load(f)
# Grab a Million Song Dataset ID from the scores dictionary 
msd_id = list(scores.keys())[1234] #this doesn't seem to select different files as you may hope
print('Million Song Dataset ID {} has {} MIDI file matches:'.format(
    msd_id, len(scores[msd_id])))
for midi_md5, score in scores[msd_id].items():
    print('  {} with confidence score {}'.format(midi_md5, score))


i = 0

while i<2:#len(scores):
    i+=1
    start = time.time()
    # Grab an MSD ID and its dictionary of matches
    msd_id, matches = scores.popitem() #removes most recently added
    # Grab a MIDI from the matches
    midi_md5, score = matches.popitem()
    # Construct the path to the aligned MIDI
    aligned_midi_path = get_midi_path(msd_id, midi_md5, 'aligned')
    # Load/parse the MIDI file with pretty_midi
    pm = pretty_midi.PrettyMIDI(aligned_midi_path)
#    # Look for a MIDI file which has lyric and key signature change events
#    if len(pm.lyrics) > 5 and len(pm.key_signature_changes) > 0:
#        break
    
    ## MIDI files in LMD-aligned are aligned to 7digital preview clips from the MSD
    ## Let's listen to this aligned MIDI along with its preview clip
    ## Load in the audio data
    #audio, fs = librosa.load(msd_id_to_mp3(msd_id))
    ## Synthesize the audio using fluidsynth
    #midi_audio = pm.fluidsynth(fs)
    ## Play audio in one channel, synthesized MIDI in the other
    #IPython.display.Audio([audio, midi_audio[:audio.shape[0]]], rate=fs)
    
    
    '''Have currently commented out all of the mp3 file shenanigans as I don't know
    what data it's meant to be using so can't begin the process. Will return to this
    in the future.'''
    
    # Retrieve piano roll of the MIDI file
    piano_roll = pm.get_piano_roll()
    
    
#    '''Extra things what Jonny Pont is fiddling with'''
#    #Histogram attempt
#    piano_hist = pm.get_pitch_class_histogram()
#    plt.hist(piano_hist,bins=12) #I need another way of plotting this. Interesting info about presence of notes.
#    
#    transition_matrix = pm.get_pitch_class_transition_matrix()
#    midi_chroma = pm.get_chroma()
#    librosa.display.specshow(midi_chroma)
    
    
    # Use 7 octaves starting from C1
    piano_roll = piano_roll[12:96]
    # Retrieve the audio corresponding to this MSD entry
    '''audio, fs = librosa.load(msd_id_to_mp3(msd_id))
    # Compute constant-Q spectrogram
    cqt = librosa.logamplitude(librosa.cqt(audio))
    # Normalize for visualization
    cqt = librosa.util.normalize(cqt)'''
    
    #not producing the plot on each iteration causes memory to eventually crash
    fig = plt.figure(figsize=(10, 6))
    plt.subplot(211)
    librosa.display.specshow(piano_roll)#, y_axis='cqt_note', cmap=plt.cm.hot)
    plt.title('MIDI piano roll')
#    plt.subplot(212)
#    '''librosa.display.specshow(cqt, y_axis='cqt_note', x_axis='time',
#                             cmap=plt.cm.hot, vmin=np.percentile(cqt, 25))'''
#    plt.title('Audio CQT');
    filename = 'chromagrams/test_midi_chromagram_playaround' + '{0:05}'.format(i) + '.png'
#    fig.savefig(filename,format='png',dpi=1200,bbox_inches='tight',pad_inches=0)
#    plt.close(fig) #without this line, the code crashed after 62 iterations...with it, closed after 89
    print(filename + ' saved')
    end = time.time()
    print( str(end-start) + ' seconds to save chromagram')

# Retrieve piano roll of one of the instruments
piano_roll = pm.instruments[2].get_piano_roll()
piano_roll = piano_roll[12:96]
fig = plt.figure(figsize=(10, 3))
librosa.display.specshow(piano_roll, y_axis='cqt_note', cmap=plt.cm.hot)
# Get the text name of this instrument's program number
program_name = pretty_midi.program_to_instrument_name(pm.instruments[2].program)
plt.title('Instrument 4 ({}) piano roll'.format(program_name));
#fig.savefig('Instrument_Note_Piano_Roll.png',format='png',dpi=1200)

# pretty_midi also provides direct access to the pitch and start/end time of each note
intervals = np.array([[note.start, note.end] for note in pm.instruments[2].notes])
notes = np.array([note.pitch for note in pm.instruments[2].notes])
fig = plt.figure(figsize=(10, 3))
mir_eval.display.piano_roll(intervals, midi=notes, facecolor='orange')
plt.title('Instrument 4 ({}) piano roll'.format(program_name))
plt.xlabel('Time')
plt.ylabel('MIDI note number');
#fig.savefig('Instrument_Midi_Piano_Roll.png')


''' Downbeats code. Doesn't work as requires access to audio. '''
'''
# Retrieve the beats and downbeats from pretty_midi
# Note that the beat phase will be wrong until the first time signature change after 0s
# So, let's start beat tracking from that point
first_ts_after_0 = [ts.time for ts in pm.time_signature_changes if ts.time > 0.][0]
# Get beats from pretty_midi, supplying a start time
beats = pm.get_beats(start_time=first_ts_after_0)
# .. downbeats, too
downbeats = pm.get_downbeats(start_time=first_ts_after_0)
# Display meter on top of waveform
plt.figure(figsize=(10, 3))
librosa.display.waveplot(audio, color='green', alpha=.5)
mir_eval.display.events(beats, base=-1, height=2, color='orange')
mir_eval.display.events(downbeats, base=-1, height=2, color='black', lw=2);
# Synthesize clicks at these downbeat times
beat_clicks = librosa.clicks(beats, length=audio.shape[0])
downbeat_clicks = librosa.clicks(downbeats, click_freq=2000, length=audio.shape[0])
IPython.display.Audio([audio, beat_clicks + downbeat_clicks], rate=fs)
'''