import json
import urllib.parse
from io import BytesIO

import requests
from twython import Twython, TwythonError

from constants.secrets import (ACCESS_SECRET, ACCESS_TOKEN, CONSUMER_KEY,
                               CONSUMER_SECRET)
from functions.photos import get_unused_photo, set_photo_used

FLICKR_REST_URL = 'https://www.flickr.com/photos/'

try:
    twitter = Twython(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_SECRET)
    photo_item = get_unused_photo()
    response = requests.get(photo_item['url_m'])
    photo = BytesIO(response.content)
    response = twitter.upload_media(media=photo)
    tweet = '«'+photo_item['title']+'»\n'+'Author: '+photo_item['ownername']+'\n'+FLICKR_REST_URL+urllib.parse.quote(photo_item['owner']+'/'+photo_item['id'])
    twitter.update_status(status=tweet, media_ids=[response['media_id']])
    set_photo_used(photo_item)
except TwythonError as e:
    print(e)
