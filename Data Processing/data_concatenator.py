# -*- coding: utf-8 -*-
"""
Created on Sat Nov 24 13:50:55 2018

@author: Jon

Script to concatenate 8 bar files from data scrape.
Methods largely made to match get_train_and_test_data.py from MIDINET.
"""

import numpy as np
from tqdm import tqdm 

train_notes  = []
train_chords = []
test_notes   = []
test_chords  = []
data_length = 2000

#Save off first 90% of data files as the training data.
for loaded in tqdm(range(int(0.9*data_length))):
    train_note_segment = np.load('8_bar_data/monophonic_data/monophonic_8bar_'+'{}'.format(loaded)+'.npy')
    train_note_segment = train_note_segment.reshape(8,1,16,128)
    train_notes.append(train_note_segment)
    
    train_chord_segment = np.load('8_bar_data/monophonic_data/chord_'+'{}'.format(loaded)+'.npy')
    train_chords.append(train_chord_segment)
            
#Save off final 10% of data files as the testing data.    
for loaded in tqdm(range(int(0.9*data_length),data_length)):
    test_segment = np.load('8_bar_data/monophonic_data/monophonic_8bar_'+'{}'.format(loaded)+'.npy')
    test_segment = test_segment.reshape(8,1,16,128)
    test_notes.append(test_segment)
    
    test_chord_segment = np.load('8_bar_data/monophonic_data/chord_'+'{}'.format(loaded)+'.npy')
    test_chords.append(test_chord_segment)

''' This isn't currently very intelligent as the test data should probably be
    picked more randomly to avoid biases. Sometimes a single song can produce 20+
    melody lines, and suddenly this has a huge impact on the results.'''    
   
train_notes  = np.vstack(train_notes)
train_chords = np.vstack(train_chords)

test_notes  = np.vstack(test_notes)
test_chords = np.vstack(test_chords)

np.save('C:/Users/jonpo/Uni/Year 4/Project/Data/train_notes_'+'{}'.format(int(0.9*data_length))+'.npy',train_notes)

np.save('C:/Users/jonpo/Uni/Year 4/Project/Data/train_chords_'+'{}'.format(int(0.9*data_length))+'.npy',train_chords)

np.save('C:/Users/jonpo/Uni/Year 4/Project/Data/test_notes_'+'{}'.format(int(0.1*data_length))+'.npy',test_notes)

np.save('C:/Users/jonpo/Uni/Year 4/Project/Data/test_chords_'+'{}'.format(int(0.1*data_length))+'.npy',test_chords)
