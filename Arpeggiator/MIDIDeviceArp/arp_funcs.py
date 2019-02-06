# -*- coding: utf-8 -*-
"""
Created on Sun Oct 28 17:20:57 2018
@author: Jon
"""

def define_root_note(midi_byte):
    modulated_note = midi_byte[1]%12
    return modulated_note


''' TAKE CHORD DEFINER FROM THE OTHER FILE AND PLACE IT HERE
    SHOULD TAKE OUTPUT OF CHORD_DETECT AND USE THAT TO MAKE A PREDICT'''


def chord_detect(note_table,root_note):

    ''' Possibly, this loading is a big time sink. I imagine more so than the iterations.'''
    import pickle
    import numpy as np

    chords_ref = pickle.load(open('hooktheory_chordnote_list.p','rb'))
    keys       = list(chords_ref.keys())

    #sort table ascending
    note_table_store = note_table
    note_table.sort(key=lambda x: x[1]) 
    count = 0

    #create empty chord matrix
    base_chord  = [[0,0,0,0]]*4
    chord_notes = []

    #build array of midi_bytes

    #only check up to 4 notes
    for note_loc in range(4):
        if note_table[note_loc][0] == 144:
            chord_notes.append((note_table[note_loc][1] - root_note)%12)
            count+=1

        #save off three notes in absence of more notes
        if count == 3 and note_table[3][0] == 0:
            break

        #save off four notes when populated
        if count == 4:
            break

        #this search condition could be made more efficient    
        if count<3 and note_loc == len(note_table):
            base_chord = [[0,0,0,0]]*4            

    ''' Subtracting the root_note, applies current note to context of scale. 
        Maths follows through logically if worked through. '''    
    # Set to numpy array for testing    
    chord_notes_vect = np.array(chord_notes)
    # chord_notes_vect = np.array([0,4,7,11])

    # Find the most similar known chord
    chord_distances = [np.inf]*len(keys)
    chosen_chord = []
    exact = 0
    for key in range(len(keys)):
        test_chord      = chords_ref[keys[key]]
        # Remove commas, convert to string, save to numpy array
        test_chord_vect = np.array([int(s) for s in test_chord.split(',')])
        if len(test_chord_vect) == len(chord_notes_vect):
            # Euclidean distance of two vectors
            dist = np.linalg.norm(chord_notes_vect-test_chord_vect)
            # if exact chord found, sorted
            if dist == 0:
                chosen_chord        = keys[key]
                exact = 1
                break
            # otherwise store off 'best of the rest'
            else:
                chord_distances[key] = dist

    # pick the most similar out of 'best of the rest'
    if chosen_chord == []:
        best_guess          = chord_distances.index(min(chord_distances))
        chosen_chord        = keys[best_guess]

    note_table = note_table_store

    return chosen_chord, exact

# note_table = [[144,46,23,0],[144,49,23,0],[144,56,23,0],[144,66,23,0],[144,43,23,0],[144,55,23,0],[144,42,23,0],[144,62,23,0],[144,76,23,0]]

# root_note = define_root_note(note_table[0])
# # root_note = define_root_note([144,78,204,0])
# [test_chord,test_chord_notes,exact] = chord_detect(note_table,root_note)
# print(test_chord)
# print(exact)

def remove_note(note_table,input_note):
    'Remove a midi note from the notetable'    
    #Remove note from the noteTable 
    empty_midi_byte = [0,0,0,0]
    for temp_midi_loc in range(len(note_table)):
        #Find OffNote message in table
        if input_note == note_table[temp_midi_loc][1]:
            #Shift every following note back up one
            for k in range(temp_midi_loc,len(note_table)-1):
                if k < len(note_table)-1:
                    note_table[k] = note_table[k+1]
    #Replace final note with empty values                
    note_table[-1] = empty_midi_byte
    return note_table

        
def add_note(note_table,new_note):
    'Add a midi note to the top of the notetable.'
    #Add note to the top of the noteTable and shift everything down one line
    for temp_midi_loc in range(len(note_table)-2,-1,-1): # -2 as final datum not important and code runs to +1
        if note_table[temp_midi_loc][2] != 0:
            note_table[temp_midi_loc+1] = note_table[temp_midi_loc]                         
    note_table[temp_midi_loc] = new_note
    note_table[0] = new_note
    return note_table


def arpeggiate_note_table(in_midi_device,out_midi_device,input_note_table,arpeggiate_type='updown',tempo=120,note_type=4):
    import time
    '''Arpeggiate the received note table'''
    empty_midi_byte = [0,0,0,0]
    output_note_table = input_note_table[:]
    
    if str(arpeggiate_type) == 'up':
        step_count = 0
        step_increase = 2
    elif str(arpeggiate_type) == 'down':
        step_count = 1
        step_increase = 2
    elif str(arpeggiate_type) == 'downup':
        step_count = 1
        step_increase = 1
    elif str(arpeggiate_type) == 'updown':    
        step_count = 0
        step_increase = 1        
    else:
        print("That is not a valid arpeggiator function")        

    current_note = empty_midi_byte
    
    '''This runs indefinitely until a new message has been received. Currently, 
    if new note on messages are received then everything is fine and dandy. 
    If new note off messages are received then the output only changes after a 
    complete loop. This means there is significant delay. I need to look into
    how the poll messages look for NoteOff and see how they differ from note on
    to see if that can give the necessary answers.
    
    This is now detecting, but the time.sleep() function means that at low tempos
    it takes a while for the off note or new on note to take effect. This makes 
    it difficutl to play with in practice.'''
    while in_midi_device.poll() == False:
        if step_count % 2 == 0:
            output_note_table.sort(key=lambda x: x[1])              #upArp
        elif step_count % 2 == 1:
            output_note_table.sort(key=lambda x: x[1],reverse=True) #downArp 
        #loop through note table and play the notes
        for note_loc in range(len(output_note_table)):
            t = time.time()
            if output_note_table[note_loc][0] == 144:
                #Don't repeat highest or lowest note. Loop on single note.
                if output_note_table[note_loc] == current_note and input_note_table[1] != empty_midi_byte:
                    continue    
                else:    
                    #play notes from output table
                    out_midi_device.write_short(output_note_table[note_loc][0],output_note_table[note_loc][1],127)
                    #evaluate code runtime - bit clunky to sleep the code
                    elapsed = time.time()-t
                    time.sleep((4/note_type)*(60/tempo)-elapsed) #sleep remaining run time
                    current_note = output_note_table[note_loc]
        #counter used to control Up/Down functionalities            
        step_count+=step_increase