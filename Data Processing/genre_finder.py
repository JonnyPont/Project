import tables
import os
import json

# Utility functions for retrieving paths
def msd_id_to_dirs(msd_id):
    """Given an MSD ID, generate the path prefix.
    E.g. TRABCD12345678 -> A/B/C/TRABCD12345678"""
    return os.path.join(msd_id[2], msd_id[3], msd_id[4], msd_id)

# h5 removed from following bracket
def msd_id_to_h5(msd_id):
    """Given an MSD ID, return the path to the corresponding h5"""
    return os.path.join(DATA_PATH, 'lmd_matched_h5',
                        msd_id_to_dirs(msd_id) + '.h5')

# Local path constants
DATA_PATH = 'C:/Users/jonpo/Uni/Year 4/Project/Data'
RESULTS_PATH = 'C:/Users/jonpo/Uni/Year 4/Project' #'results'
# Path to the file match_scores.json distributed with the LMD
# SCORE_FILE = os.path.join(RESULTS_PATH, 'match_scores.json')
SCORE_FILE = os.path.join(RESULTS_PATH, 'Python/scoresTemp27000.json')


#Get a file and check what it matches in MSD.
with open(SCORE_FILE) as f:
    scores = json.load(f)
# Grab a Million Song Dataset ID from the scores dictionary 
msd_id = list(scores.keys())[1234] #this doesn't seem to select different files as you may hope
#print('Million Song Dataset ID {} has {} MIDI file matches:'.format(
#    msd_id, len(scores[msd_id])))
#for midi_md5, score in scores[msd_id].items():
#    print('  {} with confidence score {}'.format(midi_md5, score))

with tables.open_file(msd_id_to_h5(msd_id)) as h5:
    print('ID: {}'.format(msd_id))
    print('"{}" by {} on "{}"'.format(
        h5.root.metadata.songs.cols.title[0],
        h5.root.metadata.songs.cols.artist_name[0],
        h5.root.metadata.songs.cols.release[0]))
    print(list(h5.root.metadata.artist_terms)[:5]) 
    print('Top 5 artist terms:' + str(list(h5.root.metadata.artist_terms)[:5])) #will need some string splitting to look pretty
    