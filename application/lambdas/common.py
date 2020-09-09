import time
import boto3
from datetime import datetime

bucket_name = 'task-tracker-mvp-bucket'
db_filename = 'task-tracker-db.json'

responses = {
    'no_task_name': (400, 'A task_name must be included in the request body')
}

def response_for(key):
    if not key in responses:
        raise KeyError('Response for ' + key + ' does not exist')
    else:
        key_response = responses[key]
        return {
            'statusCode': key_response[0],
            'body': key_response[1]
        }


def epoch_now():
    return time.mktime(datetime.now().timetuple())


def open_db():
    s3 = boto3.resource('s3')
    db = s3.Object(bucket_name=bucket_name, key=db_filename)
    return db
