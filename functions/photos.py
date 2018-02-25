import json

import boto3
from boto3.dynamodb.conditions import Attr, Key

TABLE_IMAGES = 'images'
DB_PROVIDER = 'dynamodb'
MAX_TITLE_LENGTH = 150

def clean_photo_data(val):
    val['used'] = 0
    val.pop('farm')
    val.pop('height_m')
    val.pop('isfamily')
    val.pop('isfriend')
    val.pop('ispublic')
    val.pop('secret')
    val.pop('server')
    val.pop('width_m')

    if val['title'] == '':
        val['title'] = 'No title'
    elif len(val['title']) > MAX_TITLE_LENGTH:
        val['title'] = val['title'][0:MAX_TITLE_LENGTH]
    return

def get_unused_photo():
    table = get_table(TABLE_IMAGES)
    db_response = table.scan(
        FilterExpression=Attr('used').eq(0)
    )
    items = db_response['Items']
    if items:
        photo_item = items[0]
    return photo_item

def set_photo_used(photo_item):
    table = get_table(TABLE_IMAGES)
    table.update_item(
    Key={
        'id': photo_item['id'],
        'dateadded' : photo_item['dateadded']
    },
    UpdateExpression='SET used = :used',
    ExpressionAttributeValues={
                ':used': 1,
            },
    )
    return

def get_table(val):
    dynamodb = boto3.resource(DB_PROVIDER)
    table = dynamodb.Table(val)
    return table

def load_photos():
    table = get_table(TABLE_IMAGES)
    with table.batch_writer() as batch:
        with open('data.json', 'r') as data_file:
            data = json.load(data_file)
            for val in data:
                batch.put_item(val)
