import json
import os

import boto3

from functions.photos import load_photos

#Loads data.json to dynamodb table Images
load_photos()