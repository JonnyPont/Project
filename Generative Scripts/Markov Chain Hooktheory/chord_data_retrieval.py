# -*- coding: utf-8 -*-
"""
Created on Mon Nov  5 13:08:54 2018

@author: jp15101
"""

import requests
from requests_oauthlib import OAuth2Session


#''' This first section logs into the site and retrieves the access token for 
#    making any future requests. Doesn't need to be run more than once. Remember
#    to set the password.'''
#header = {"Accept": "application/json", 
#          "Content-Type": "application/json",
#          "username":"jp15101",
#          "password": "-"}
#
#base_url = "https://api.hooktheory.com/v1/" 
#post_url = "users/auth"
#chord_prob_url = "trends/nodes"
#r = requests.post(base_url+post_url,data=header)
#activkey_value = r.json()['activkey']
#client_id = r.json()['id']
#print(r.json())




''' Basic script for making a pull request.  '''
base_url = "https://api.hooktheory.com/v1/" 
chord_prob_url = "trends/nodes"
chord_extension = "?cp=4,1,7" #gets probabilities given preceeding chord IV. Separate with commas for longer progessions eg 1,4,1,5
get_header = {'Authorization':'Bearer 63f32052def743e24b54f09172819e73'}
#10 requests every 10 seconds
new_request = requests.get(base_url+chord_prob_url+chord_extension,headers=get_header) #,timeout=0.1 might be a good parameter to add in case of duff calls
current_data = new_request.json()

'''Checks for total probs. Will have to normalise probs as some sum to >1 and 
   some to <1. Both are problematic for the markov model.'''
prob_sum=0
for i in range(len(current_data)):
    prob_sum = prob_sum + current_data[i]['probability']
    
print(prob_sum)
print(new_request.status_code)
chord_probs = new_request.text

#header2 =   {
#                'Accept': 'application/json', 
#                'Authorization': 'Bearer 63f32052def743e24b54f09172819e73', 
#                'Content-Type': 'application/json'
#            }

#Authorization = ['Bearer' ] 

#Authorization = {"Bearer": activkey_value}
#        "Header Value": "Bearer" + str(activkey_value)}
#x = requests.get(base_url+chord_prob_url,params=Authorization)



