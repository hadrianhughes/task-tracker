import json
import boto3

responses = {
    'no_task_name': (400, 'A task_name must be included in the request body')
}

def responseFor(key):
    if not key in responses:
        raise KeyError('Response for ' + key + ' does not exist')
    else:
        key_response = responses[key]
        return {
            'statusCode': key_response[0],
            'body': key_response[1]
        }


def add_task_session(task_name):
    try:
        s3 = boto3.resource('s3')
        db = s3.Object(bucket_name='task-tracker-mvp-bucket', key='task-tracker-db.json')
        dbResponse = db.get()
        data = dbResponse['Body'].read()
    except:
        print('Something went wrong when accessing the S3 Bucket')

    json_data = json.loads(data)
    sessions = json_data['sessions']

    if len(sessions) == 0:
        sessions.append({ 'task_name': task_name })
        db.put(Body=json.dumps({ 'sessions': sessions }))


def lambda_handler(event, context):
    if event['body'] == None:
        return responseFor('no_task_name')

    body = json.loads(event['body'])

    if 'task_name' in body:
        task_name = body['task_name']
    else:
        return responseFor('no_task_name')

    add_task_session(task_name)

    return { 'statusCode': 200 }
