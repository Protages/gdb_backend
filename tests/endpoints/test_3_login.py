import pytest

from fastapi.testclient import TestClient


@pytest.mark.order(3)
def test_login_valid_data(test_client: TestClient):
    request_data = {
        'username': 'User_2',
        'password': 'mypass'
    }
    response_data = {
        'user': {
            'id': 2,
            'email': 'user.2@gmail.com',
            'username': 'User_2',
            'about': '',
            'rating': 0,
            'is_active': True,
            'is_superuser': False,
            'is_email_confirmed': False,
            'roles': []
        },
        'token': {
            'access_token': 'some_token',
            'token_type': 'baerer'
        }
    }
    response = test_client.post('/token', data=request_data)
    print('-----', response.json())
    assert response.status_code == 200
    assert response.json()['user'] == response_data['user']
    assert response.json()['token']['token_type'] == \
           response_data['token']['token_type']
    assert response.json()['token'].get('access_token', False)
    assert len(response.json()['token'].get('access_token')) > 15
