import pytest

from start import app

@pytest.fixture()
def apigw_event():
    return {}

def test_lambda_handler(apigw_event):
    response = app.lambda_handler(apigw_event)

    assert response["statusCode"] == 200
