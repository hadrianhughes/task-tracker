import json
from common import response_for, open_db, epoch_now, format_response

def stop_task_session():
    try:
        db = open_db()
        dbResponse = db.get()
        data = dbResponse['Body'].read()
    except:
        return response_for('s3_error')

    json_data = json.loads(data)
    sessions = json_data['sessions']
    last_session = sessions[-1] if len(sessions) > 0 else None

    if not last_session or 'stop' in last_session:
        return response_for('no_current_task')

    last_session['stop'] = epoch_now()
    db.put(Body=json.dumps({ 'sessions': sessions }))

    return (200, '')


def lambda_handler(event, context):
    status_code, message = stop_task_session()
    return format_response(status_code, message)
