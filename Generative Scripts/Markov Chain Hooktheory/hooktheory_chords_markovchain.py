# -*- coding: utf-8 -*-
"""
Created on Tue Nov 20 17:13:36 2018

@author: Jon

This should be a MARKOV CHAIN!
"""

import pickle
import pandas as pd
import numpy as np
import random
import bisect
import pygame.midi

import arp_funcs_data as af
from note_detector_data import determine_note


def play_chord(out_midi_device,notes,reference_note=60):
    
    #Creates an empty note table 
    empty_midi_byte = [0,0,0,0]
    input_note_table = [empty_midi_byte] * 10
    
    notes = notes.split(',')
    notes = [int(note)+reference_note for note in notes]
    for note in range(1,len(notes)):
        if notes[note] < notes[note-1]:
            notes[note] += 12 #make a note the next octave up if it loops over the end of the scale
    
    for note in range(len(notes)):
        input_note_table[note]= [144,notes[note],127,0]
        
    af.arpeggiate_note_table(out_midi_device,input_note_table,'updown',tempo=75,note_type=8)
        

chord_to_notes = {'1' : '0,4,7',
'142' : '11,0,4,7',
'143' : '7,11,0,4',
'16' : '4,7,0',
'164': '7,0,4',
'165' : '4,7,11,0',
'17' : '0,4,7,11',
'2' : '2,5,9',
'242' : '0,2,5,9',
'243' : '9,0,2,5',
'26' : '5,9,2',
'264' : '9,2,5',
'265' : '5,9,0,2',
'27' : '2,5,9,0',
'3' : '4,7,11',
'342' : '2,4,7,11',
'343' : '11,2,4,7',
'36' : '7,11,4',
'364' : '11,4,7',
'365' : '7,11,2,4',
'37' : '4,7,11,2',
'4' : '5,9,0',
'4/2' : '7,11,2',
'4/3' : '9,1,4',
'442' : '4,5,9,0',
'443' : '0,4,5,9',
'46' : '9,0,5',
'46/5' : '4,7,0',
'46/6' : '6,9,2',
'464' : '0,5,9',
'464/4' : '5,10,2',
'465' : '9,0,4,5',
'47' : '5,9,0,4',
'47/3' : '9,1,4,8',
'47/4' : '10,2,5,9',
'5' : '7,11,2',
'5/2' : '9,1,4',
'5/3' : '11,3,6',
'5/5' : '2,6,9',
'5/6' : '4,8,11',
'5/7' : '6,10,1',
'542' : '5,7,11,2',
'542/3' : '9,11,3,6',
'542/4' : '10,0,4,7',
'542/5' : '0,2,6,9',
'542/6' : '2,4,8,11',
'543' : '2,5,7,11',
'543/3' : '6,9,11,3',
'543/4' : '7,10,0,4',
'543/5' : '9,0,2,6',
'56' : '11,2,7',
'56/2' : '1,4,9',
'56/3' : '3,6,11',
'56/4' : '4,7,0',
'56/5' : '6,9,2',
'56/6' : '8,11,4',
'564' : '2,7,11',
'564/2' : '4,9,1',
'564/3' : '6,11,3',
'564/4' : '7,0,4',
'564/6' : '11,4,8',
'565' : '11,2,5,7',
'565/2' : '1,4,7,9',
'565/3' : '3,6,9,11',
'565/4' : '4,7,10,0',
'565/5' : '6,9,0,2',
'565/6' : '8,11,2,4',
'57' : '7,11,2,5',
'57/2' : '9,1,4,7',
'57/3' : '11,3,6,9',
'57/4' : '0,4,7,10',
'57/5' : '2,6,9,0',
'57/6' : '4,8,11,2',
'57/7' : '6,10,1,4',
'6' : '9,0,4',
'642' : '7,9,0,4',
'643' : '4,7,9,0',
'66' : '0,4,9',
'664' : '4,9,0',
'665' : '0,4,7,9',
'67' : '9,0,4,7',
'7' : '11,2,5',
'7/2' : '1,4,7',
'7/3' : '3,6,9',
'7/5' : '6,9,0',
'7/6' : '8,11,2',
'76' : '2,5,11',
'76/4' : '7,10,4',
'77' : '11,2,5,9',
'77/2' : '1,4,7,11',
'77/5' : '6,9,0,4',
'C1' : '0,3,6',
'C16' : '3,6,0',
'C2' : '1,5,8',
'C3' : '3,6,10',
'C5' : '6,10,1',
'C57' : '6,10,1,5',
'C6' : '8,0,3',
'C67' : '8,0,3,6',
'D2' : '2,5,9',
'D26' : '5,9,2',
'D3' : '3,7,10',
'D4' : '5,9,0',
'D47' : '5,9,0,3',
'D5' : '7,10,2',
'D56' : '10,2,7',
'D6' : '9,0,3',
'D77' : '10,2,5,9',
'L26' : '6,9,2',
'L264' : '9,2,6',
'L265' : '6,9,0,2',
'L27' : '2,6,9,0',
'L3' : '4,7,11',
'L4' : '6,9,0',
'L5' : '7,11,2',
'L542' : '6,7,11,2',
'L56' : '11,2,7',
'L57' : '7,11,2,6',
'L6' : '9,0,4',
'L67' : '9,0,4,7',
'L7' : '11,2,6',
'L764' : '6,11,2',
'L765' : '2,6,9,11',
'L77' : '11,2,6,9',
'M142' : '10,0,4,7',
'M143' : '7,10,0,4',
'M164' : '7,0,4',
'M17' : '0,4,7,10',
'M4' : '5,9,0',
'M5' : '7,10,2',
'M56' : '10,2,7',
'M57' : '7,10,2,5',
'M67' : '9,0,4,7',
'M76' : '2,5,10',
'M77' : '10,2,5,9',
'Y2' : '1,5,8',
'Y3' : '3,7,10',
'Y37' : '3,7,10,1',
'Y4' : '5,8,0',
'Y5' : '7,10,1',
'Y6' : '8,0,3',
'b1' : '0,3,7',
'b16' : '3,7,0',
'b165' : '3,7,10,0',
'b17' : '0,3,7,10',
'b2' : '2,5,8',
'b26' : '5,8,2',
'b27' : '2,5,8,0',
'b3' : '3,7,10',
'b36' : '7,10,3',
'b37' : '3,7,10,2',
'b4' : '5,8,0',
'b46' : '8,0,5',
'b464' : '0,5,8',
'b465' : '8,0,3,5',
'b47' : '5,8,0,3',
'b5' : '7,10,2',
'b56' : '10,2,7',
'b564' : '2,7,10',
'b565' : '10,2,5,7',
'b57' : '7,10,2,5',
'b6' : '8,0,3',
'b66' : '0,3,8',
'b67' : '8,0,3,7',
'b7' : '10,2,5',
'b76' : '2,5,10',
'b77' : '10,2,5,8'}

first_order_chords  = pickle.load(open("first_order_chords_normalised.p","rb"))
keys                = list(first_order_chords.keys())
keys_sorted         = sorted(keys)

''' Loop through all of the data.'''
trans_mat = np.zeros([len(keys_sorted),len(keys_sorted)])

for key in keys_sorted:    
    ''' For key, find the prob of relative key. Find in numpy matrix and replace
        the value present.'''   
    for i in range(len(first_order_chords[key])):    
        ''' This has not been tested, but the logic is sound. '''
        input_chord_loc     = keys_sorted.index(key) #location of input chord
        output_chord        = first_order_chords[key][i]['chord_ID'] #Value of output chord
        output_prob         = first_order_chords[key][i]['probability'] #probability of output chord
        '''Check the chord exists in the list. This means that not all my 
           row probabilities add to 1. Not sure if this is an issue or not. In 
           time it will be worth normalising this.'''
        if output_chord in keys_sorted:
            output_chord_loc    = keys_sorted.index(first_order_chords[key][i]['chord_ID']) #index of output chord    
            trans_mat[input_chord_loc][output_chord_loc] = output_prob
        
''' Save the transition matrix as a csv file for Giphy '''
''' This is currently saving off the transition probabilities. I wonder if it 
    would be possible to save no of instances of chord change rather than 
    just the probability? I'll probs have to pull different data from HookTheory'''

trans_mat_df = pd.DataFrame(trans_mat,index=keys_sorted,columns=keys_sorted)
trans_mat_df.to_csv('transition_matrix.csv')

''' Make a normalised random input chord vector. Attempt to weight it in the 
    direction of a certain chord in the list. '''
current_state = [0]*len(keys_sorted)
#for i in range(len(keys_sorted)):
#    current_state[i] = random.random()
#current_state[0] = 1    #bias towards this chord? Testing seems to prove this is the case.
current_state[14] = 1
prob_factor      = 1/sum(current_state)
current_state    = [prob_factor * p for p in current_state]


#Separate midi functions, controllers, outputs need to be defined
pygame.midi.init()
output_id = pygame.midi.get_default_output_id()
out_midi_device = pygame.midi.Output(output_id)

''' Generate a chord sequence following a markov chain. '''
for chord in range(2):
    ''' Roulette wheel sampler '''
    seed = random.random()        
    index_for_now = bisect.bisect_left(np.cumsum(current_state),seed)-1 #Finds insertion point. I want value one before insertion point.
    print(keys_sorted[index_for_now])
    notes = chord_to_notes[keys_sorted[index_for_now]]
    print(notes)
    play_chord(out_midi_device,notes)
    current_state = trans_mat.dot(current_state)
    
    ''' Most likely chord - gets stuck sometimes '''
#    max_value = max(current_state)
#    max_index = list(current_state).index(max_value)
#    print(keys_sorted[max_index])
#    notes = chord_to_notes[keys_sorted[max_index]]
#    play_chord(out_midi_device,notes)
#    current_state = trans_mat.dot(current_state)
    
pygame.midi.quit()   