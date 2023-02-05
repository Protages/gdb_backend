# After all these tests, we have roles with id: 2

import pytest

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session


@pytest.mark.parametrize(
    'request_data, response_data',
    [
        ({
            'title': 'Role 1'
        }, {
            'id': 1,
            'title': 'Role 1'
        }),
        ({
            'title': 'Role 2'
        }, {
            'id': 2,
            'title': 'Role 2'
        }),
    ]
)
def test_create_role(test_client: TestClient, request_data, response_data):
    response = test_client.post('/api/v1/role', json=request_data)
    print('-----', response.json())
    assert response.status_code == 201
    assert response.json() == response_data


def test_create_role_invalid_data(test_client: TestClient):
    request_data = {
        'bar': 'baz'
    }
    response = test_client.post('/api/v1/role', json=request_data)
    print('-----', response.json())
    assert response.status_code == 422


def test_read_role(test_client: TestClient):
    response_data = {
        'id': 1,
        'title': 'Role 1'
    }
    response = test_client.get(f'/api/v1/role/{1}')
    print('-----', response.json())
    assert response.status_code == 200
    assert response.json() == response_data


def test_read_role_invalid_id(test_client: TestClient):
    response_data = {
        'detail': 'Role does not exist'
    }
    response = test_client.get(f'/api/v1/role/{999}')
    print('-----', response.json())
    assert response.status_code == 400
    assert response.json() == response_data


def test_read_all_role(test_client: TestClient):
    response_data = [
        {
            'id': 1,
            'title': 'Role 1'
        },
        {
            'id': 2,
            'title': 'Role 2'
        }
    ]
    response = test_client.get(f'/api/v1/role/all/')
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
def test_read_all_role_invalid_pagination(
        test_client: TestClient, size, page, response_data
    ):
    response = test_client.get(f'/api/v1/role/all/?size={size}&page={page}')
    print('-----', response.json())
    assert response.status_code == 400
    assert response.json() == response_data


def test_update_role(test_client: TestClient):
    request_data = {
        'title': 'Role 1 update'
    }
    response_data = {
        'id': 1,
        'title': 'Role 1 update'
    }
    response = test_client.put(f'/api/v1/role/{1}', json=request_data)
    print('-----', response.json())
    assert response.status_code == 200
    assert response.json() == response_data


def test_update_role_invalid_id(test_client: TestClient):
    request_data = {
        'title': 'Role 1 update'
    }
    response_data = {
        'detail': 'Role does not exist'
    }
    response = test_client.put(f'/api/v1/role/{999}', json=request_data)
    print('-----', response.json())
    assert response.status_code == 400
    assert response.json() == response_data


def test_update_role_invalid_data(test_client: TestClient):
    request_data = {
        'bar': 'baz'  # We can send any key-value, it's ok
    }
    response_data = {
        'id': 1,
        'title': 'Role 1 update'
    }
    response = test_client.put(f'/api/v1/role/{1}', json=request_data)
    print('-----', response.json())
    assert response.status_code == 200
    assert response.json() == response_data


def test_delete_role(test_client: TestClient):
    response = test_client.delete(f'/api/v1/role/{1}')
    assert response.status_code == 204


def test_delete_role_invalid_id(test_client: TestClient):
    response_data = {
        'detail': 'Role does not exist'
    }
    response = test_client.delete(f'/api/v1/role/{999}')
    print('-----', response.json())
    assert response.status_code == 400
    assert response.json() == response_data
