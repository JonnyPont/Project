# -*- coding: utf-8 -*-
"""
Created on Tue Nov 20 10:48:51 2018

@author: Jon

Retrieve activkey ie. log in credentials from Hooktheory.

"""

import requests


''' This logs into the site and retrieves the access token for making any 
    future requests. Doesn't need to be run more than once. Remember to set the
    password.'''
    
header = {"Accept": "application/json", 
          "Content-Type": "application/json",
          "username":"jp15101",
          "password": "-"}

base_url = "https://api.hooktheory.com/v1/" 
post_url = "users/auth"
r = requests.post(base_url+post_url,data=header)
activkey_value = r.json()['activkey']
client_id = r.json()['id']
print(r.json())

