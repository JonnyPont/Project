# -*- coding: utf-8 -*-
"""
Created on Tue Nov  6 23:43:15 2018

@author: Jon
"""

import pickle

chord_changes = pickle.load(open('chord_change_probabilities.p','rb'))

keys = chord_changes.keys()

prec_chord_seq = list(chord_changes.loc[:,keys[0]])
prec_chord = list(chord_changes.loc[:,keys[1]])
next_chord = list(chord_changes.loc[:,keys[2]])
probability = list(chord_changes.loc[:,keys[3]])

diff_prec_chords = list(set(prec_chord)) #74 different chords
del diff_prec_chords[46] # A wild none-type had appeared
diff_next_chords = list(set(next_chord)) #169 different chords



chord_relations = []
my_dict = {}

'''
#I think I need an extra nested loop
for i in range(len(diff_prec_chords)):
    for j in range(1,len(prec_chord)):
        probabilities_list = []
        for k in range(len(diff_next_chords)):
            if diff_prec_chords[i] == prec_chord[j] and next_chord[j] == diff_next_chords[k]:
                probabilities_list.append(probability[j])
            chord_transition = diff_prec_chords[i] + ' to ' + next_chord[j]        
            my_dict[chord_transition] = probabilities_list
'''                
            
for i in range(len(diff_prec_chords)):
    probabilities_list = []
    for j in range(1,len(prec_chord)):
        if diff_prec_chords[i] == prec_chord[j]:
            probabilities_list.append(probability[j])
        chord_transition = diff_prec_chords[i] + ' to ' + next_chord[j]        
        my_dict[chord_transition] = probabilities_list            
            

'''
Loop through diff_prec_chords:
    Loop through prec_chord:
        if diff == prec:
            find probability of the next chord given previous by making a list of
            probabilities.
            Will probs have to be a list of lists.
            OR MAYBE A DICTIONARY - BUT THAT INVOLVES SOME GOOD THINKING.
'''