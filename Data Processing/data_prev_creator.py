import numpy as np 
import os
from tqdm import tqdm

file_root = 'C:/Users/jonpo/Uni/Year 4/Project/Python/8_bar_data'


# file_no = 0
# while file_no<119975: 242038

for file_no in tqdm(range(242038)):
    open_file = os.path.join(file_root,'polyphonic_data/polyphonic_8bar_'+'{}'.format(file_no)+'.npy')
    save_file = os.path.join(file_root,'polyphonic_data/polyphonic_prev8bar_'+'{}'.format(file_no)+'.npy')

    current_bars = np.load(open_file)

    #current  8 bars: 1,2,3,4,5,6,7,8
    #previous 8 bars: 0,1,2,3,4,5,6,7

    previous_bars = [None]*8
    previous_bars[0] = np.zeros([128,16]) #first bar is null

    for i in range(len(current_bars)-1):
        previous_bars[i+1] = current_bars[i]

    np.save(save_file,previous_bars)
    # file_no += 1
    # print(file_no)