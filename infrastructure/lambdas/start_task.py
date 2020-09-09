import json
import boto3
from utils import response_for, epoch_now

bucket_name = 'task-tracker-mvp-bucket'
db_filename = 'task-tracker-db.json'

def add_task_session(task_name):
    try:
        s3 = boto3.resource('s3')
        db = s3.Object(bucket_name=bucket_name, key=db_filename)
        dbResponse = db.get()
        data = dbResponse['Body'].read()
    except:
        print('Something went wrong when accessing the S3 Bucket')

    json_data = json.loads(data)
    sessions = json_data['sessions']
    sessions_count = len(sessions)
    last_session = sessions[-1] if sessions_count > 0 else None
    now = epoch_now()

    if last_session and not 'stop' in last_session:
        if last_session['task_name'] == task_name:
            return 304
        else:
            last_session['stop'] = now

    sessions.append({ 'task_name': task_name, 'start': now })
    db.put(Body=json.dumps({ 'sessions': sessions }))

    return 200


def lambda_handler(event, context):
    if event['body'] == None:
        return response_for('no_task_name')

    body = json.loads(event['body'])

    if 'task_name' in body:
        task_name = body['task_name']
    else:
        return response_for('no_task_name')

    status_code = add_task_session(task_name)

    return { 'statusCode': status_code }
