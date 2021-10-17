import requests
import urllib3
import facebook 
import os 
import json 

path = os.getcwd()
key_path = path[:-11]+'facebook.txt'

def return_token(my_path): 
    with open(key_path) as f:
        lines = f.readlines()
        token = lines[-1]
        return token
token = return_token(key_path)

graph = facebook.GraphAPI(access_token= token, version = 2.8)   #ERROR: Application does not have the capability to make this API call.
events = graph.request('/search?q=Poetry&type=event&limit=10')

#Note: è un errore dato dai requisiti di accesso del profilo da developer. TO DO !
 