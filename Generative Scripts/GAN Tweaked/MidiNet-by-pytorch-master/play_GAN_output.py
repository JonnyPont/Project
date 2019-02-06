import numpy as np 

my_song = np.load('output_songs.npy')
interest = my_song[0][4]
print(interest)