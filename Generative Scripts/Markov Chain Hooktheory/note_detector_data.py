# -*- coding: utf-8 -*-
"""
Created on Sun Oct 28 18:54:54 2018

@author: Jon
"""

def determine_note(midi_byte):

    note_played = midi_byte[1]
    if note_played%12 == 0:
        note = "C"
        print(note)
    elif note_played%12 == 1:
        note = "C#"
        print(note)    
    elif note_played%12 == 2:
        note = "D"
        print(note)
    elif note_played%12 == 3:
        note = "D#"
        print(note)
    elif note_played%12 == 4:
        note = "E"
        print(note)
    elif note_played%12 == 5:
        note = "F"
        print(note)
    elif note_played%12 == 6:
        note = "F#"
        print(note)
    elif note_played%12 == 7:
        note = "G"
        print(note)     
    elif note_played%12 == 8:
        note = "G#"
        print(note)
    elif note_played%12 == 9:
        note = "A"
        print(note)     
    elif note_played%12 == 10:
        note = "A#"
        print(note)
    elif note_played%12 == 11:
        note = "B"
        print(note)          
        
    return note