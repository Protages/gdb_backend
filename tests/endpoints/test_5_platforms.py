# After all these tests, we have platforms with id: 1, 2, 3, 4

import pytest

from fastapi.testclient import TestClient

from tests.endpoints.data import platforms_data


@pytest.mark.parametrize(
    'request_data, response_data',
    [(a, b) for a, b in zip(
        platforms_data.create_platform_valid_data,
        platforms_data.platform_valid_data_response
    )]
)
def test_create_platform(test_client: TestClient, request_data, response_data):
    response = test_client.post('/api/v1/platform', json=request_data)
    print('-----', response.json())
    assert response.status_code == 201
    assert response.json() == response_data


def test_create_platform_invalid_data(test_client: TestClient):
    request_data = platforms_data.create_platform_invalid_data
    response_data = platforms_data.create_platform_invalid_data_response
    response = test_client.post('/api/v1/platform', json=request_data)
    print('-----', response.json())
    assert response.status_code == 422
    assert response.json() == response_data


def test_read_platform(test_client: TestClient):
    response_data = platforms_data.platform_valid_data_response[0]
    response = test_client.get(f'/api/v1/platform/{1}')
    print('-----', response.json())
    assert response.status_code == 200
    assert response.json() == response_data


def test_read_platform_invalid_id(test_client: TestClient):
    response_data = platforms_data.platform_invalid_id_response
    response = test_client.get(f'/api/v1/platform/{999}')
    print('-----', response.json())
    assert response.status_code == 400
    assert response.json() == response_data


def test_read_all_platform(test_client: TestClient):
    response_data = platforms_data.platform_valid_data_response
    response = test_client.get(f'/api/v1/platform/')
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
    response = test_client.get(f'/api/v1/platform/?size={size}&page={page}')
    print('-----', response.json())
    assert response.status_code == 400
    assert response.json() == response_data


def test_update_platform(test_client: TestClient):
    request_data = platforms_data.update_platform_valid_data
    response_data = platforms_data.update_platform_valid_data_response
    response = test_client.put(f'/api/v1/platform/{5}', json=request_data)
    print('-----', response.json())
    assert response.status_code == 200
    assert response.json() == response_data


def test_update_platform_invalid_id(test_client: TestClient):
    request_data = platforms_data.update_platform_valid_data
    response_data = platforms_data.platform_invalid_id_response
    response = test_client.put(f'/api/v1/platform/{999}', json=request_data)
    print('-----', response.json())
    assert response.status_code == 400
    assert response.json() == response_data


def test_update_platform_invalid_data(test_client: TestClient):
    request_data = platforms_data.create_platform_invalid_data
    response_data = platforms_data.create_platform_invalid_data_response
    response = test_client.put(f'/api/v1/platform/{1}', json=request_data)
    print('-----', response.json())
    assert response.status_code == 422
    assert response.json() == response_data


def test_delete_platform(test_client: TestClient):
    response = test_client.delete(f'/api/v1/platform/{4}')
    assert response.status_code == 204

    response = test_client.get(f'/api/v1/platform/')
    assert response.status_code == 200
    assert len(response.json()) == 4


def test_delete_platform_invalid_id(test_client: TestClient):
    response_data = platforms_data.platform_invalid_id_response
    response = test_client.delete(f'/api/v1/platform/{999}')
    print('-----', response.json())
    assert response.status_code == 400
    assert response.json() == response_data
