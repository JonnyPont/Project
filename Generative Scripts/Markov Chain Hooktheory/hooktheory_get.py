# -*- coding: utf-8 -*-
"""
Created on Tue Nov 20 10:51:21 2018

@author: Jon
"""

import requests
import time
import pickle

chord_prob_url = 'trends/nodes'
get_header = {'Authorization':'Bearer 63f32052def743e24b54f09172819e73'}
chord_url_base = '?cp='
base_url = "https://api.hooktheory.com/v1/" 
first_order_chords = {}

''' Make a list of all of the different chords I want to look up '''

''' This is the list of chords from the 5000 song dataset on github.'''

all_chords=['5/3','5/6','143','57','Y6','Y5','3','L265','5/5','L7','542/6','77/2',
 '564','56/2','16','77','M57','57/3','C3','66','564/6','D2','76','165','57/4',
 '565/4','D47','C57','56/6','342','Y37','343','7/2','543/3','76/4','7/6','L57',
 '47/4','M77','D77','b5','C6','b77','D6','b564','443','364','7/5','Y4','142','5/7',
 'D5','L264','442','464/4','D3','b1','243','565/3','4/3','b465','M164','37','56/5',
 'L77','464/7','565','265','642','242','7','b4','M67','543','1','M143','C67',
 '56/4','b565','M17','264','57/2','57/7','57/6','542','C2','4','b6','b67','47',
 '164','L764','643','M76','56','L765','5','543/4','564/4','b56','b36','M56','b7',
 'D56','543/5','b2','b46','Y2','565/5','L67','5/2','46','46/5','b165','L56','664',
 'M4','M5','b57','7/3','b3','6','542/3','b16','665','L3','365','564/2','564/3',
 'Y3','46/6','47/3','L27','27','L6','C1','C5','17','b464','L5','36','b66', 'D26',
 '464','b17','56/3','b26','L26','57/5','2','565/2','26','M142','C16','L4','b37',
 '77/5','565/6','b27','b76','4/2','542/4','D4','b47','L542','67','542/5', '465']
 
''' Get data for each starting chord.'''
for i in range(len(all_chords)):
    chord_extension = chord_url_base+all_chords[i]
    x = requests.get(base_url+chord_prob_url+chord_extension,headers=get_header)
    ''' Add each piece of data to a dictionary.'''
    if x.json() == []:
        print(x.status_code)
        print(all_chords[i])
    else:
        print('Chord data available')
    first_order_chords[chord_extension[4:]] = x.json()
    #On the 10th iteration sleep for 10 seconds for twitter API
    if i%10 == 9:
        print('Sleeping for 11 secs')
        time.sleep(11)
    
#Not tested but this should run. - executed in command bar not script for current file
pickle.dump(first_order_chords,open("first_order_chords.p","wb"))