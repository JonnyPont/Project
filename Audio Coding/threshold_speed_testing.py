# -*- coding: utf-8 -*-
"""
Created on Wed Feb 20 14:41:30 2019

@author: HPTest
"""
import numpy as np

x = np.load('sample.npy')
y = np.load('sample.npy')
z = np.load('sample.npy')

#def test():
#    "Stupid test function"
#    for i in range(16):
#        for j in range(128):
#            if x[0][0][i][j] < x[0][0][i].max():
#                x[0][0][i][j] = 0     
#            else: 
#                x[0][0][i][j]=1

def test():
    new_mat2 = np.zeros(y.shape)
    for i in range(16):
        new_mat2[0][0][i][y[0][0][i].argmax()]=1
        
#def test():
#    new_mat3 = np.sign(z[0][0]-z[0][0].max(1,keepdims=True))+1
        
def test():
    new_mat3 = np.sign(z[0][0] - z[0][0].max(1,keepdims=True)) +1

if __name__=='__main__':
    from timeit import Timer
    t = Timer("test()", "from __main__ import test")
    print(t.timeit(1000000))
    
    
    

#
#
#start_time = time.time()
#for i in range(16):
#    for j in range(128):
#        if x[0][0][i][j] < x[0][0][i].max():
#            x[0][0][i][j] = 0     
#        else: 
#            x[0][0][i][j]=1
#end_time = time.time()
#time_elapse = end_time-start_time
#
#
#end_time2 = time.time()
#time_elapse2 = end_time2-start_time2