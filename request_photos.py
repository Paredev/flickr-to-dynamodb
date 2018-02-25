import json

import requests
from requests.auth import HTTPDigestAuth

from constants.flickr import *
from constants.secrets import FLICKR_API_KEY
from functions.photos import clean_photo_data

data = {"api_key": FLICKR_API_KEY,
        "extras": EXTRAS,
        "format": REQUEST_FORMAT,
        "group_id": GROUP_ID, 
        "media": MEDIA,
        "method": METHOD,  
        "nojsoncallback": NO_JSON_CALLBACK,
        "page": PAGE,
        "per_page": PER_PAGE,
        }

response = requests.get(FLICKR_API_ENDPOINT, data)

if response.ok:
    response_json = response.json()
    photos_list = []
    for photo in response_json['photos']['photo']:
        #Only photos with direct url are valid
        if photo['url_m'] is not None:
            clean_photo_data(photo)
            photos_list.append(photo)
    with open('data.json', 'w') as outfile:
            json.dump(photos_list, outfile)
else:
    print("Error: "+response.status_code)
