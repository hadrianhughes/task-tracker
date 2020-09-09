import json

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

def lambda_handler(event, context):
    if event['body'] == None:
        return responseFor('no_task_name')

    body = json.loads(event['body'])

    if 'task_name' in body:
        task_name = body['task_name']
    else:
        return responseFor('no_task_name')

    return { 'statusCode': 200 }
