from bs4 import BeautifulSoup
import urllib3
import certifi
import pandas as pd
import re
import numpy as np
import urllib.parse
data2 = np.load('data.npy')
tot_genre = []

for i in range(100):

    #Names of song and Artist (to be looped through in the dataset)
    song_name = str(data2[0][i].decode('utf-8'))
    Artist = str(data2[1][i].decode('utf-8'))
    #print('Artist: ' + Artist)
    #print('Song: ' + song_name)
    #print(Artist)
    Artist = urllib.parse.quote_plus(Artist)
    song_name = urllib.parse.quote_plus(song_name)
    
    #Replacing the spaces with +'s to fit the url structure
    song_name = song_name.replace(" ", "+")
    Artist = Artist.replace(" ", "+")
    
    #Currently using last fm for scraping
    url = ('https://www.last.fm/music/' + Artist + '/_/' + song_name)
    
    #list of core genres we want to investigate
    genre_list = ('pop', 'jazz', 'classical', '80s', 'metal', 'punk', 'rock', 'blues', 'country', 'dance', 'electronic', 'hip-hop', 'rap', 'indie', 'opera', 'r&b', 'reggae')
    
    #initialising an empty array to later contain the core genre of each song
    genre_class = []
    
    #Check the certification of the site (avoids a warning)
    http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where() )
    
    #Return the html script
    response = http.request('GET', url)
    soup = BeautifulSoup(response.data, "lxml")
    #Extract the part of the script relating to the genre tags (currently
    #also contains all other info relating to song such as name, artist etc.)
    genre = soup.find_all("div", {"class": "hidden"})
    
    #Strip this down so it contins only the genre info
    genre = re.search('"tag": "(.+?)"', str(genre[0]))
    
    print('-----GENRE-----')
    
    #Find the genre's that fall into our core list
    i=0
    for each_genre in genre_list:
        if each_genre in str(genre):
            genre_class.append(each_genre)
            print(genre_class[i])
            i+=1
    if genre_class == []:
        print(Artist,song_name)
            
    tot_genre.append(genre_class)
            
            
#df['genre'] = tot_genre

#Later - setup a dataframe to append the genre to the main dataset
Columns = ['Artist', 'Song Title', 'Genre']

