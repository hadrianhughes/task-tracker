import pytest

from start import app

def test_lambda_handler(apigw_event):
    response = app.lambda_handler(apigw_event)

    assert response["statusCode"] == 200
