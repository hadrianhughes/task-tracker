import json
from common import response_for, epoch_now, open_db, format_response

def add_task_session(task_name):
    try:
        db = open_db()
        dbResponse = db.get()
        data = dbResponse['Body'].read()
    except:
        return response_for('s3_error')

    json_data = json.loads(data)
    sessions = json_data['sessions']
    last_session = sessions[-1] if len(sessions) > 0 else None
    now = epoch_now()

    if last_session and not 'stop' in last_session:
        if last_session['task_name'] == task_name:
            return (304, '')
        else:
            last_session['stop'] = now

    sessions.append({ 'task_name': task_name, 'start': now })
    db.put(Body=json.dumps({ 'sessions': sessions }))

    return (200, '')


def lambda_handler(event, context):
    if event['body'] == None:
        return response_for('no_task_name')

    body = json.loads(event['body'])

    if not 'task_name' in body:
        return response_for('no_task_name')

    task_name = body['task_name']
    status_code, message = add_task_session(task_name)

    return format_response(status_code, message)
