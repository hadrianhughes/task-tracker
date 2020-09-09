import pytest
import json

from start_task import app

def test_no_body():
    response = app.lambda_handler({ 'body': None }, '')

    assert response['statusCode'] == 400


def test_no_task_name():
    response = app.lambda_handler({
        'body': json.dumps({ 'foo': 'bar' })
    }, '')

    assert response['statusCode'] == 400


def test_happy_path():
    response = app.lambda_handler({
        'body': json.dumps({ 'task_name': 'testName1' })
    }, '')

    assert response['statusCode'] == 200
