import pytest

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session


create_user_valid_data = [
    {  # Max data
        'email': 'user.1@gmail.com',
        'about': 'About user 1',
        'rating': 1,
        'is_active': False,
        'is_superuser': True,
        'username': 'User_1',
        'password': 'mypass',
        'roles': []
    },
    {  # Min data
        'email': 'user.2@gmail.com',
        'username': 'User_2',
        'password': 'mypass',
        'roles': []
    }
]

create_user_valid_data_response = [
    {
        'id': 1,
        'email': 'user.1@gmail.com',
        'username': 'User_1',
        'about': 'About user 1',
        'rating': 1,
        'is_active': False,
        'is_superuser': True,
        'is_email_confirmed': False,
        'roles': []
    },
    {
        'id': 2,
        'email': 'user.2@gmail.com',
        'username': 'User_2',
        'about': '',
        'rating': 0,
        'is_active': True,
        'is_superuser': False,
        'is_email_confirmed': False,    
        'roles': []
    }
]

create_user_invalid_email_data = [
    {
        'email': '@gmail.com',
        'username': 'User_3',
        'password': 'mypass',
        'roles': []
    },
    {
        'email': 'user.3@',
        'username': 'User_3',
        'password': 'mypass',
        'roles': []
    },
    {
        'email': 'user.3gmail.com',
        'username': 'User_3',
        'password': 'mypass',
        'roles': []
    },
]

create_user_invalid_username_data = [
    {
        'email': 'user.3@gmail.com',
        'username': 'Use',  # Min 4 charters
        'password': 'mypass',
        'roles': []
    },
    {
        'email': 'user.3@gmail.com',
        'username': '_User_3',  # No _,- or . at the beginning
        'password': 'mypass',
        'roles': []
    },
    {
        'email': 'user.3@gmail.com',
        'username': 'User_3_',  # No _,- or . at the end 
        'password': 'mypass',
        'roles': []
    },
]

create_user_invalid_password_data = [
    {
        'email': 'user.3@gmail.com',
        'username': 'User_3',
        'password': 'pass',  # At least 6 characters
        'roles': []
    },
    {
        'email': 'user.3@gmail.com',
        'username': 'User_3',
        'password': 'пароль',  # Latin characters only
        'roles': []
    },
    {
        'email': 'user.3@gmail.com',
        'username': 'User_3',
        'password': '0123456789',  # At least one letter
        'roles': []
    },
]

update_user_valid_data = {
    'about': 'New about',
    'rating': 11,
    'is_active': True,
    'is_superuser': False,
    'password': 'user1newpass',
    'roles': []
}
update_user_valid_data_response = {
    'id': 1,
    'username': 'User_1',
    'email': 'user.1@gmail.com',
    'about': 'New about',
    'rating': 11,
    'is_active': True,
    'is_superuser': False,
    'is_email_confirmed': False,
    'roles': []
}


@pytest.mark.parametrize(
    'request_data, response_data',
    [
        (create_user_valid_data[0], {
            'user': create_user_valid_data_response[0],
            'token': {
                'access_token': 'some_token',
                'token_type': 'baerer'
            }
        }),
        (create_user_valid_data[1], {
            'user': create_user_valid_data_response[1],
            'token': {
                'access_token': 'some_token',
                'token_type': 'baerer'
            }
        }),
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


@pytest.mark.parametrize(
    'response_data',
    [{
        'detail': [
            {
                'loc': ['body', 'email'], 
                'msg': 'Email is not valid', 
                'type': 'value_error'
            }
        ]
    }]
)
@pytest.mark.parametrize('request_data', create_user_invalid_email_data)
def test_create_user_invalid_email(test_client: TestClient, request_data, response_data):
    response = test_client.post('/api/v1/user', json=request_data)
    print('-----', response.json())
    assert response.status_code == 422
    assert response.json() == response_data


def test_create_user_invalid_unique_email(test_client: TestClient):
    request_data = {
        'email': 'user.1@gmail.com',  # Alredy exist
        'username': 'User_3',
        'password': 'mypass',
        'roles': []
    }
    response_data = {'detail': 'email field must be uniqe'}
    response = test_client.post('/api/v1/user', json=request_data)
    print('-----', response.json())
    assert response.status_code == 400
    assert response.json() == response_data


@pytest.mark.parametrize(
    'response_data',
    [{
        'detail': [
            {
                'loc': ['body', 'username'],
                'msg': 'Username is not valid',
                'type': 'value_error'
            }
        ]
    }]
)
@pytest.mark.parametrize('request_data', create_user_invalid_username_data)
def test_create_user_invalid_username(
        test_client: TestClient, request_data, response_data
    ):
    response = test_client.post('/api/v1/user', json=request_data)
    print('-----', response.json())
    assert response.status_code == 422
    assert response.json() == response_data


def test_create_user_invalid_unique_username(test_client: TestClient):
    request_data = {
        'email': 'user.3@gmail.com',
        'username': 'User_1',  # Alredy exist
        'password': 'mypass',
        'roles': []
    }
    response_data = {'detail': 'username field must be uniqe'}
    response = test_client.post('/api/v1/user', json=request_data)
    print('-----', response.json())
    assert response.status_code == 400
    assert response.json() == response_data


@pytest.mark.parametrize(
    'response_data',
    [{
        'detail': [
            {
                'loc': ['body', 'password'],
                'msg': 'Password is not valid',
                'type': 'value_error'
            }
        ]
    }]
)
@pytest.mark.parametrize('request_data', create_user_invalid_password_data)
def test_create_user_invalid_password(
        test_client: TestClient, request_data, response_data
    ):
    response = test_client.post('/api/v1/user', json=request_data)
    print('-----', response.json())
    assert response.status_code == 422
    assert response.json() == response_data


def test_read_user(test_client: TestClient):
    response_data = create_user_valid_data_response[0]
    response = test_client.get(f'/api/v1/user/{1}')
    print('-----', response.json())
    assert response.status_code == 200
    assert response.json() == response_data


def test_read_user_invalid_id(test_client: TestClient):
    response_data = {'detail': 'User does not exist'}
    response = test_client.get(f'/api/v1/user/{999}')
    print('-----', response.json())
    assert response.status_code == 400
    assert response.json() == response_data


def test_read_all_user(test_client: TestClient):
    response_data = create_user_valid_data_response
    response = test_client.get(f'/api/v1/user/all/')
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
    response = test_client.get(f'/api/v1/user/all/?size={size}&page={page}')
    print('-----', response.json())
    assert response.status_code == 400
    assert response.json() == response_data


def test_update_user(test_client: TestClient):
    request_data = update_user_valid_data
    response_data = update_user_valid_data_response
    response = test_client.put(f'/api/v1/user/{1}', json=request_data)
    print('-----', response.json())
    assert response.status_code == 200
    assert response.json() == response_data


def test_update_user_invalid_id(test_client: TestClient):
    request_data = {'about': 'New about'}
    response_data = {'detail': 'User does not exist'}
    response = test_client.put(f'/api/v1/user/{999}', json=request_data)
    print('-----', response.json())
    assert response.status_code == 400
    assert response.json() == response_data


@pytest.mark.parametrize(
    'response_data',
    [{
        'detail': [
            {
                'loc': ['body', 'password'],
                'msg': 'Password is not valid',
                'type': 'value_error'
            }
        ]
    }]
)
@pytest.mark.parametrize('request_data', create_user_invalid_password_data)
def test_update_user_invalid_password(
        test_client: TestClient, request_data, response_data
    ):
    response = test_client.put(f'/api/v1/user/{1}', json=request_data)
    print('-----', response.json())
    assert response.status_code == 422
    assert response.json() == response_data


def test_delete_user(test_client: TestClient):
    response = test_client.delete(f'/api/v1/user/{1}')
    assert response.status_code == 204


def test_delete_user_invalid_id(test_client: TestClient):
    response_data = {'detail': 'User does not exist'}
    response = test_client.delete(f'/api/v1/user/{999}')
    print('-----', response.json())
    assert response.status_code == 400
    assert response.json() == response_data
