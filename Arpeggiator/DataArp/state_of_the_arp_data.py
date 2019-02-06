# -*- coding: utf-8 -*-
"""
Created on Sun Oct 28 17:51:18 2018

@author: Jon
"""

import pygame

import pygame.midi

import time

import arp_funcs as af

from note_detector import determine_note

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
                determine_note(new_note)
                input_note_table = af.add_note(input_note_table,new_note)
            elif midi_events[new_midi][0][0] == 128: #if note off
                removal_note = midi_events[new_midi][0][1]
                input_note_table = af.remove_note(input_note_table,removal_note)

            #print input noteTable for viewing reference
            for byte in input_note_table:
                print(*byte)    
            print('\n') 
        
        af.arpeggiate_note_table(in_midi_device,out_midi_device,input_note_table,'updown',tempo=120,note_type=8)
        

#Close off all of the opened channels and exit the initialisations.
in_midi_device.close()

pygame.midi.quit()

pygame.quit()