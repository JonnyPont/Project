import numpy as np


#Take song
#Find song title and artist from MSD
#Pull genre tag from discogs using this info
#Save off 8 bars, using naming and counting of genre. eg rock_monophonic_23.npy, soul_monophonic_1.npy
#I think classes are a good way of getting around the problem. But I have never done it before so dunno.


class genre:

    def __init__(self,data):
        self.data = data
        self.size = len(data)

