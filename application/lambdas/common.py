import time
import boto3
from datetime import datetime

bucket_name = 'task-tracker-mvp-bucket'
db_filename = 'task-tracker-db.json'

responses = {
    'no_task_name': (400, 'A task_name must be included in the request body'),
    's3_error': (500, 'An error occurred while attempting to access to S3 bucket'),
    'no_current_task': (409, 'Not currently working on a task')
}

def response_for(key):
    if not key in responses:
        raise KeyError('Response for ' + key + ' does not exist')
    else:
        return responses[key]

def format_response(status_code, message):
    return { 'statusCode': status_code, 'body': message }


def epoch_now():
    return time.mktime(datetime.now().timetuple())


def open_db():
    s3 = boto3.resource('s3')
    db = s3.Object(bucket_name=bucket_name, key=db_filename)
    return db
