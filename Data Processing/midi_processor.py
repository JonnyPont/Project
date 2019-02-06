# -*- coding: utf-8 -*-
"""
Created on Mon Oct 15 13:54:00 2018
@author: jp15101
https://github.com/kushalbhabra/pyMidi/blob/master/src/test.py
"""

import pygame

import pygame.midi

import time

def remove_note(note_table,input_note):
    'Remove a midi note from the notetable'    
    #Remove note from the noteTable 
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


def arpeggiate_note_table(input_note_table,arpeggiate_type):
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
    to see if that can give the necessary answers.'''
    while in_midi_device.poll() == False:
        if step_count % 2 == 0:
            output_note_table.sort(key=lambda x: x[1])              #upArp
        elif step_count % 2 == 1:
            output_note_table.sort(key=lambda x: x[1],reverse=True) #downArp 
        #loop through note table and play the notes
        for note_loc in range(len(output_note_table)):
            if output_note_table[note_loc][0] == 144:
                #Don't play a note if it's the same as the last note played and there are other notes available.
                #Removes repeats of high notes. Causes single notes to be played on repeat.
                if output_note_table[note_loc] == current_note and input_note_table[1] != empty_midi_byte:
                    continue    
                else:    
                    #play notes from output table
                    out_midi_device.write_short(output_note_table[note_loc][0],output_note_table[note_loc][1],127)
                    #evaluate code runtime
                    elapsed = time.time()-t
                    #IT would be better to wait for the remaining amount of time. If code has run for 0.1 secs
                    #already then we want it to only wait 0.1 secs. for example
                    all_times.append(elapsed)
                    time.sleep(0.2)
                    current_note = output_note_table[note_loc]
        #counter used to control Up/Down functionalities            
        step_count+=step_increase


#Needs initialising for some reason, and declaring that events need to be got
pygame.init()
pygame.fastevent.init()
event_get = pygame.fastevent.get
event_post = pygame.fastevent.post

#Separate midi functions, controllers, outputs need to be defined
pygame.midi.init()
input_id = pygame.midi.get_default_input_id()
output_id = pygame.midi.get_default_output_id()

in_midi_device = pygame.midi.Input( input_id )
out_midi_device = pygame.midi.Output(output_id)

#Creates an empty note table 
empty_midi_byte = [0,0,0,0]
input_note_table = [empty_midi_byte] * 10

#Little code test speed nugget
all_times = []

#Run forever
while True:
#    if a message exists
    if in_midi_device.poll():
        t = time.time()
#        store the first 10 new midi messages
        midi_events = in_midi_device.read(10)
        
        #Little code for turning off the programme from the midi controller.
        if midi_events[0][0] == [144, 72, 1, 0]:
            break
        
        #print received midi messages and 
        for new_midi in range(len(midi_events)):
            if midi_events[new_midi][0][0] == 144: #if note on
                new_note = midi_events[new_midi][0]
                input_note_table = add_note(input_note_table,new_note)
            elif midi_events[new_midi][0][0] == 128: #if note off
                removal_note = midi_events[new_midi][0][1]
                input_note_table = remove_note(input_note_table,removal_note)

            #print input noteTable for viewing reference
            for byte in input_note_table:
                print(*byte)    
            print('\n') 
        
        arpeggiate_note_table(input_note_table,'up')
        

#Close off all of the opened channels and exit the initialisations.
in_midi_device.close()

pygame.midi.quit()

pygame.quit()