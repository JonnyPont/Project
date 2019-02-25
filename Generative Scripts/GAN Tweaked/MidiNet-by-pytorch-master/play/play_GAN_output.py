import numpy as np 
import pygame.midi
import arp_funcs_data as af
import time

def play_chord(out_midi_device,notes):
    
    #Creates an empty note table 
    empty_midi_byte = [0,0,0,0]
    input_note_table = [empty_midi_byte] * 16
    
    notes = [int(note) for note in notes]
    print(len(notes))
    for note in range(len(notes)):
        input_note_table[note]= [144,notes[note],127,0]
        
    af.arpeggiate_note_table(out_midi_device,input_note_table,'updown',tempo=75,note_type=8)

# my_song = np.load('output_songs.npy')
# interest = my_song[0][4]
# print(interest)

pygame.midi.quit()   

#Separate midi functions, controllers, outputs need to be defined
pygame.midi.init()
output_id = pygame.midi.get_default_output_id()
out_midi_device = pygame.midi.Output(output_id)

#This doesn't quite work yet but remove the for loop and just load in sample, will play. Try to fix this.
chords = np.load('output_songs.npy')
samples = np.load('sample.npy')

for i in range(8):
    sample = chords[0][i][0][0].detach().numpy()
    temp_mat = np.sign(sample - sample.max(1,keepdims=True)) +1
    notes = list(np.argmax(temp_mat,axis=1))

#    play_chord(out_midi_device,notes)
    # time.sleep(5)

    for note in notes:
        out_midi_device.write_short(144,note,127)
        time.sleep(0.5)
    
    '''I don't need this here, but this is how to send multiple bytes of midi 
        data to the output device. Dunno why the timestamp doesn't work'''
#    for note in notes:
#        out_midi_device.write([[[144,73,127,0],1000],[[144,75,127,0],1000]])
#        time.sleep(0.5)
    
pygame.midi.quit()   








# ##This works:
# samples = np.load('sample.npy')
# temp_mat = np.sign(samples[0][0] - samples[0][0].max(1,keepdims=True)) +1
# notes = list(np.argmax(temp_mat,axis=1))

# #Separate midi functions, controllers, outputs need to be defined
# pygame.midi.init()
# output_id = pygame.midi.get_default_output_id()
# out_midi_device = pygame.midi.Output(output_id)

# play_chord(out_midi_device,notes)
