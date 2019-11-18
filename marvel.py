#!/usr/bin/env python3

import requests
from requests.exceptions import HTTPError
import hashlib
import time
import json
pub = "ef9f5ba9be9ce136050e4ffadca9f21a"
priv = "0d919ca33667999901aca937157de75da8a3e1e2"
ts=str(time.time())
storynum="36864";
message=ts+priv+pub
h=hashlib.md5(message.encode())
url = "http://gateway.marvel.com/v1/public/stories/"+storynum+"?apikey="+pub+"&hash="+h.hexdigest()+"&ts="+ts
#url="http://gateway.marvel.com/v1/public/comics/17618"+"?apikey="+pub+"&hash="+h.hexdigest()+"&ts="+ts
        

try:
    response = requests.get(url)
    print(json.dumps(response.json(),sort_keys=True,indent=4,separators=(',',': ')))
    response.raise_for_status()
    
except HTTPError as http_err:
    print('HTTP error has occurred: ',http_err)
    
except Exception as err:
    print('some other error has occurred: ',err)
else:
    print('success')\
    
    
        
    
