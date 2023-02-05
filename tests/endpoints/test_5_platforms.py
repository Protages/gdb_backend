# After all these tests, we have platforms with id: 2

import pytest

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session


@pytest.mark.parametrize(
    'request_data, response_data',
    [
        ({
            'title': 'Platform 1'
        }, {
            'id': 1,
            'title': 'Platform 1'
        }),
        ({
            'title': 'Platform 2'
        }, {
            'id': 2,
            'title': 'Platform 2'
        }),
    ]
)
def test_create_platform(test_client: TestClient, request_data, response_data):
    response = test_client.post('/api/v1/platform', json=request_data)
    print('-----', response.json())
    assert response.status_code == 201
    assert response.json() == response_data


def test_create_platform_invalid_data(test_client: TestClient):
    request_data = {
        'bar': 'baz'
    }
    response_data = {
        'detail': [
            {
                'loc': ['body', 'title'], 
                'msg': 'field required', 
                'type': 'value_error.missing'
            }
        ]
    }
    response = test_client.post('/api/v1/platform', json=request_data)
    print('-----', response.json())
    assert response.status_code == 422
    assert response.json() == response_data


def test_read_platform(test_client: TestClient):
    response_data = {
        'id': 1,
        'title': 'Platform 1'
    }
    response = test_client.get(f'/api/v1/platform/{1}')
    print('-----', response.json())
    assert response.status_code == 200
    assert response.json() == response_data


def test_read_platform_invalid_id(test_client: TestClient):
    response_data = {
        'detail': 'Platform does not exist'
    }
    response = test_client.get(f'/api/v1/platform/{999}')
    print('-----', response.json())
    assert response.status_code == 400
    assert response.json() == response_data


def test_read_all_platform(test_client: TestClient):
    response_data = [
        {
            'id': 1,
            'title': 'Platform 1'
        },
        {
            'id': 2,
            'title': 'Platform 2'
        }
    ]
    response = test_client.get(f'/api/v1/platform/all/')
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
def test_read_all_platform_invalid_pagination(
        test_client: TestClient, size, page, response_data
    ):
    response = test_client.get(f'/api/v1/platform/all/?size={size}&page={page}')
    print('-----', response.json())
    assert response.status_code == 400
    assert response.json() == response_data


def test_update_platform(test_client: TestClient):
    request_data = {
        'title': 'Platform 1 update'
    }
    response_data = {
        'id': 1,
        'title': 'Platform 1 update'
    }
    response = test_client.put(f'/api/v1/platform/{1}', json=request_data)
    print('-----', response.json())
    assert response.status_code == 200
    assert response.json() == response_data


def test_update_platform_invalid_id(test_client: TestClient):
    request_data = {
        'title': 'Platform 1 update'
    }
    response_data = {
        'detail': 'Platform does not exist'
    }
    response = test_client.put(f'/api/v1/platform/{999}', json=request_data)
    print('-----', response.json())
    assert response.status_code == 400
    assert response.json() == response_data


def test_update_platform_invalid_data(test_client: TestClient):
    request_data = {
        'bar': 'baz'
    }
    response_data = {
        'detail': [
            {
                'loc': ['body', 'title'], 
                'msg': 'field required', 
                'type': 'value_error.missing'
            }
        ]
    }
    response = test_client.put(f'/api/v1/platform/{1}', json=request_data)
    print('-----', response.json())
    assert response.status_code == 422
    assert response.json() == response_data


def test_delete_platform(test_client: TestClient):
    response = test_client.delete(f'/api/v1/platform/{1}')
    assert response.status_code == 204


def test_delete_platform_invalid_id(test_client: TestClient):
    response_data = {
        'detail': 'Platform does not exist'
    }
    response = test_client.delete(f'/api/v1/platform/{999}')
    print('-----', response.json())
    assert response.status_code == 400
    assert response.json() == response_data
