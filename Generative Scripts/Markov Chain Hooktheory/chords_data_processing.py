# -*- coding: utf-8 -*-
"""
Created on Tue Nov  6 18:25:06 2018

@author: Jon
"""
import pandas as pd
import pickle

some_chords = pd.read_csv('some_chords.csv',encoding='ISO-8859-1')

for i in range(len(some_chords)):
    chord_IDs = list(some_chords.loc[:,'chord_ID'])
    L1 = list(some_chords.loc[:,'L1'])
    child_path = list(some_chords.loc[:,'child_path'])
    probability = list(some_chords.loc[:,'probability'])

preceeding_chord_seq = [None]*len(some_chords)
preceeding_chord = [None]*len(some_chords)
# Cheeky lil attept here. VERY pseudocode atm.
for i in range(1,len(preceeding_chord)): # first entry is null
    preceeding_chord_seq[i] = child_path[i].replace(',' + chord_IDs[i],'')
    preceeding_chord[i] = preceeding_chord_seq[i].split(',')[-1]


d = {'prec_chord_seq':preceeding_chord_seq,'prec_chord':preceeding_chord,
     'next_chord':chord_IDs,'probability':probability}

df = pd.DataFrame(d,columns=['prec_chord_seq','prec_chord','next_chord','probability'])    

pickle.dump(df,open("chord_change_probabilities.p","wb"))