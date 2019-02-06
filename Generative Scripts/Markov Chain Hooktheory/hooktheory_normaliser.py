# -*- coding: utf-8 -*-
"""
Created on Tue Nov 20 11:17:08 2018

@author: Jon
"""


import pickle

first_order_chords = pickle.load(open("first_order_chords.p","rb"))
del first_order_chords['464/7'] #one empty string exists so needs deleting
keys= list(first_order_chords.keys())


''' Loop through all of the data.'''
for key in keys:
    prob_sum=0
    probs_list = [None]*len(first_order_chords[key])
    for i in range(len(first_order_chords[key])):
        probs_list[i] = first_order_chords[key][i]['probability']
    ''' Normalise probabilities '''    
    prob_factor = 1/sum(probs_list)
    probs_list = [prob_factor * p for p in probs_list]
    ''' Replace probs in the dict with normalised probs '''
    for i in range(len(first_order_chords[key])):
        first_order_chords[key][i]['probability'] = probs_list[i]
        
pickle.dump(first_order_chords,open("first_order_chords_normalised.p","wb"))