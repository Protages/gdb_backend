# After all these tests, we have users with id: 1, 2, 3, 4

import pytest

from fastapi.testclient import TestClient

from tests.endpoints.data import user_data


@pytest.mark.parametrize(
    'request_data, response_data',
    [
        (a, {
            'user': b,
            'token': {
                'access_token': 'some_token',
                'token_type': 'baerer'
            }
        }) for a, b in zip(
            user_data.create_user_valid_data, user_data.user_valid_data_response
        )
    ]
)
def test_create_user(test_client: TestClient, request_data, response_data):
    response = test_client.post('/api/v1/user', json=request_data)
    print('-----', response.json())
    assert response.status_code == 201
    assert response.json()['user'] == response_data['user']
    assert response.json()['token']['token_type'] == response_data['token']['token_type']
    assert response.json()['token'].get('access_token', False)
    assert len(response.json()['token'].get('access_token')) > 15


@pytest.mark.parametrize('response_data', [user_data.user_invalid_email_response])
@pytest.mark.parametrize('request_data', user_data.create_user_invalid_email_data)
def test_create_user_invalid_email(test_client: TestClient, request_data, response_data):
    response = test_client.post('/api/v1/user', json=request_data)
    print('-----', response.json())
    assert response.status_code == 422
    assert response.json() == response_data


def test_create_user_invalid_unique_email(test_client: TestClient):
    request_data = user_data.create_user_invalid_unique_email_data
    response_data = {'detail': 'email field must be uniqe'}
    response = test_client.post('/api/v1/user', json=request_data)
    print('-----', response.json())
    assert response.status_code == 400
    assert response.json() == response_data


@pytest.mark.parametrize('response_data', [user_data.user_invalid_username_response])
@pytest.mark.parametrize('request_data', user_data.create_user_invalid_username_data)
def test_create_user_invalid_username(
        test_client: TestClient, request_data, response_data
    ):
    response = test_client.post('/api/v1/user', json=request_data)
    print('-----', response.json())
    assert response.status_code == 422
    assert response.json() == response_data


def test_create_user_invalid_unique_username(test_client: TestClient):
    request_data = user_data.create_user_invalid_unique_username_data
    response_data = {'detail': 'username field must be uniqe'}
    response = test_client.post('/api/v1/user', json=request_data)
    print('-----', response.json())
    assert response.status_code == 400
    assert response.json() == response_data


@pytest.mark.parametrize('response_data', [user_data.user_invalid_password_response])
@pytest.mark.parametrize('request_data', user_data.create_user_invalid_password_data)
def test_create_user_invalid_password(
        test_client: TestClient, request_data, response_data
    ):
    response = test_client.post('/api/v1/user', json=request_data)
    print('-----', response.json())
    assert response.status_code == 422
    assert response.json() == response_data


def test_read_user(test_client: TestClient):
    response_data = user_data.user_valid_data_response[0]
    response = test_client.get(f'/api/v1/user/{1}')
    print('-----', response.json())
    assert response.status_code == 200
    assert response.json() == response_data


def test_read_user_invalid_id(test_client: TestClient):
    response_data = user_data.user_invalid_id_response
    response = test_client.get(f'/api/v1/user/{999}')
    print('-----', response.json())
    assert response.status_code == 400
    assert response.json() == response_data


def test_read_all_user(test_client: TestClient):
    response_data = user_data.user_valid_data_response
    response = test_client.get(f'/api/v1/user/')
    print('-----', response.json())
    assert response.status_code == 200
    assert response.json() == response_data


@pytest.mark.parametrize(
    'size, page, response_data',
    [
        (-10, 0, {'detail': 'The pagination size parameter must be >= 0'}),
        (0, -10, {'detail': 'The pagination page parameter must be >= 0'}),
    ]
)
def test_read_all_user_invalid_pagination(
        test_client: TestClient, size, page, response_data
    ):
    response = test_client.get(f'/api/v1/user/?size={size}&page={page}')
    print('-----', response.json())
    assert response.status_code == 400
    assert response.json() == response_data


def test_update_user(test_client: TestClient):
    request_data = user_data.update_user_valid_data
    response_data = user_data.update_user_valid_data_response
    response = test_client.put(f'/api/v1/user/{5}', json=request_data)
    print('-----', response.json())
    assert response.status_code == 200
    assert response.json() == response_data


def test_update_user_invalid_id(test_client: TestClient):
    request_data = {'about': 'New about'}
    response_data = user_data.user_invalid_id_response
    response = test_client.put(f'/api/v1/user/{999}', json=request_data)
    print('-----', response.json())
    assert response.status_code == 400
    assert response.json() == response_data


@pytest.mark.parametrize('response_data', [user_data.user_invalid_password_response])
@pytest.mark.parametrize('request_data', user_data.create_user_invalid_password_data)
def test_update_user_invalid_password(
        test_client: TestClient, request_data, response_data
    ):
    response = test_client.put(f'/api/v1/user/{1}', json=request_data)
    print('-----', response.json())
    assert response.status_code == 422
    assert response.json() == response_data


def test_delete_user(test_client: TestClient):
    response = test_client.delete(f'/api/v1/user/{5}')
    assert response.status_code == 204

    response = test_client.get(f'/api/v1/user/')
    assert response.status_code == 200
    assert len(response.json()) == 4


def test_delete_user_invalid_id(test_client: TestClient):
    response_data = user_data.user_invalid_id_response
    response = test_client.delete(f'/api/v1/user/{999}')
    print('-----', response.json())
    assert response.status_code == 400
    assert response.json() == response_data
