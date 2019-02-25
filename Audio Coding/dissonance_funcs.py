''' Test parameters put in to discuss the issue of f1 near to 220Hz. Seems like
    a significant oversight '''

def add_harmonics(input_note,no_of_harmonics):
    
    fundamental_frequency = 440*(2**((input_note-69)/12)) #midi to frequency
    complex_tone = [fundamental_frequency*idx for idx in range(1,no_of_harmonics+2)] #fundamental plus n harmonics

    return complex_tone

def absolute_dissonance(freq1,freq2):
    
    import math
    
    C0 = 65
    k0 = 1
    switch = False
    '''Ensure correct labelling of frequencies. We require freq_1 to be the 
        lower frequency. '''
    if freq1 <= freq2:
        freq_1 = freq1
        freq_2 = freq2        
    elif freq1 > freq2:
        freq_1 = freq2
        freq_2 = freq1
        switch = True
    
    freq_b   = 2.27*freq_1**0.477
    freq_dif = freq_2 - freq_1
    
    base = math.e

    if freq_1 == freq_2:
        dyad_dissonance = 75
    elif (freq_2/freq_1)%1==0:
        dyad_dissonance = 0 #250
    elif freq_dif <= freq_b:
        dyad_dissonance = k0*(100*((2+math.log(freq_dif/freq_1,base))/(2+math.log(freq_b/freq_1,base)))+C0)
    elif freq_b < freq_dif and freq_dif <= freq_1:
        dyad_dissonance = k0*(90*(math.log(freq_dif/freq_1,base))/(math.log(freq_b/freq_1,base))+10+C0)
    elif freq_2 > 2*freq_1:
        dyad_dissonance = k0*C0
    
    return dyad_dissonance, switch

def pressure_dissonance(p1,p2,dyad_dissonance):

    # From paper part I
    p0  = 57    # p0  = 2*10**-1.15
    n_e = 0.2
    n_l = 0.32
    n_h = 0.15

    if p1 == p2:
        dyad_dissonance = dyad_dissonance*(p1/p0)**n_e
    elif p1 > p2:
        dyad_dissonance = dyad_dissonance*((p1/p0)**n_e)*(p2/p1)**n_h
    elif p1 < p2:
        dyad_dissonance = dyad_dissonance*((p2/p0)**n_e)*(p1/p2)**n_l

    return dyad_dissonance

def total_dissonance(input_notes,no_of_harmonics):
    
    beta = 0.25    
    input_note_list = [item for sublist in input_notes for item in sublist]        
    
    summation = 0
    test_list = []
    sound_pressure = [45,57,57,53,49,45,43,41]

    for i in range(len(input_note_list)):
        for j in range(i + 1, len(input_note_list)):
            [real_abs_diss_dyads,switch] = absolute_dissonance(input_note_list[i], input_note_list[j])
            if switch:
                p2 = sound_pressure[i%no_of_harmonics]
                p1 = sound_pressure[j%no_of_harmonics]                        
            elif not switch:
                p1 = sound_pressure[i%no_of_harmonics]
                p2 = sound_pressure[j%no_of_harmonics]        
            real_abs_diss_dyads = pressure_dissonance(p1,p2,real_abs_diss_dyads)
            if real_abs_diss_dyads >1000:
                print(input_note_list[i])
                print(input_note_list[j])
            # if real_abs_diss_dyads > 165:
            #     real_abs_diss_dyads = 165
            test_list.append(real_abs_diss_dyads)
            summation += (real_abs_diss_dyads)**(1/beta) #+ 65**(1/beta)           
    total_diss = summation**beta
    # total_diss = total_diss/len(test_list)     
    # total_diss = sum(test_list)/len(test_list)
    
    return total_diss,test_list

import matplotlib.pyplot as plt
import numpy as np

note = 69
no_of_harmonics = 8
notes_per_octave = 48
octave_no = 1
division = notes_per_octave/12*octave_no
values = list()

#two tone dissonance test
for i in range(notes_per_octave*octave_no):
    [diss,test] = total_dissonance([add_harmonics(note,no_of_harmonics),add_harmonics(note+(i*12/notes_per_octave),no_of_harmonics)],no_of_harmonics)
    values.append(diss)

# #THIS WORKS! It determines the overall dissonance of the tones
# [diss,test] = total_dissonance([add_harmonics(note,1),add_harmonics(note+12,1)])
# print(diss)
# # values.append(diss)

# #Vary a single note over a dyad
# for i in range(resolution):
#    [diss,test] = total_dissonance([add_harmonics(note,no_of_harmonics),add_harmonics(note+7,no_of_harmonics),add_harmonics(note+i,no_of_harmonics)])    
#    values.append(diss)
    
# plt.plot(values)    
plt.plot(np.arange(0,12*octave_no,12/notes_per_octave),values)
plt.xticks(np.arange(0,(12*octave_no)+1,1.0))
plt.xlabel('Semitones of separation')
plt.ylabel('Consonance')
plt.show()