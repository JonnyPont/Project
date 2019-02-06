#FIRST: pip install discogs_client
import discogs_client as dc
import numpy as np
from tqdm import tqdm
import time
import csv
import pickle

ds = dc.Client('/find_genre/1.0', user_token='YNwyLvHlapVHyZWnigBSOMRiiMLUpKuyPAESeLDT')

data2=np.load('data.npy')

genre_list2=[]

for i in tqdm(range(200,225)): #200,len(data2[0]))):
    song_data = data2[0][i]     # Song Title
    artist_data = data2[1][i]   # Artist Name
    track_data = data2[12][i]   # 
    results = ds.search(str(artist_data)  + ' - ' + str(song_data), type = 'release')
    try:
        genre = results[0].genres
    except IndexError:
        genre = []
    genre_list2.append([track_data, genre])
    time.sleep(0.6)
    
    
with open('discogs_genre_list5.pkl','wb') as handle:
    pickle.dump(genre_list2, handle, protocol=pickle.HIGHEST_PROTOCOL)

