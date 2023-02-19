# After all these tests, we have roles with id: 1, 2, 3, 4

import pytest

from fastapi.testclient import TestClient

from tests.endpoints.data import roles_data


@pytest.mark.order(1)
@pytest.mark.parametrize(
    'request_data, response_data',
    [(a, b) for a, b in zip(
        roles_data.create_role_valid_data, roles_data.role_valid_data_response
    )]
)
def test_create_role(test_client: TestClient, request_data, response_data):
    response = test_client.post('/api/v1/role', json=request_data)
    print('-----', response.json())
    assert response.status_code == 201
    assert response.json() == response_data


def test_create_role_invalid_data(test_client: TestClient):
    request_data = roles_data.create_role_invalid_data
    response = test_client.post('/api/v1/role', json=request_data)
    print('-----', response.json())
    assert response.status_code == 422
    assert response.json() == roles_data.create_role_invalid_data_response


def test_read_role(test_client: TestClient):
    response_data = roles_data.role_valid_data_response[0]
    response = test_client.get(f'/api/v1/role/{1}')
    print('-----', response.json())
    assert response.status_code == 200
    assert response.json() == response_data


def test_read_role_invalid_id(test_client: TestClient):
    response_data = roles_data.role_invalid_id_response
    response = test_client.get(f'/api/v1/role/{999}')
    print('-----', response.json())
    assert response.status_code == 400
    assert response.json() == response_data


def test_read_all_role(test_client: TestClient):
    response_data = roles_data.role_valid_data_response
    response = test_client.get('/api/v1/role/')
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
    response = test_client.get(f'/api/v1/role/?size={size}&page={page}')
    print('-----', response.json())
    assert response.status_code == 400
    assert response.json() == response_data


def test_update_role_unused_field(test_client: TestClient):
    request_data = {
        'bar': 'baz'  # We can send any key-value, it's ok
    }
    response_data = roles_data.role_valid_data_response[0]
    response = test_client.put(f'/api/v1/role/{1}', json=request_data)
    print('-----', response.json())
    assert response.status_code == 200
    assert response.json() == response_data


def test_update_role(test_client: TestClient):
    request_data = roles_data.update_role_valid_data
    response_data = roles_data.update_role_valid_data_response
    response = test_client.put(f'/api/v1/role/{1}', json=request_data)
    print('-----', response.json())
    assert response.status_code == 200
    assert response.json() == response_data


def test_update_role_invalid_id(test_client: TestClient):
    request_data = roles_data.update_role_valid_data
    response_data = roles_data.role_invalid_id_response
    response = test_client.put(f'/api/v1/role/{999}', json=request_data)
    print('-----', response.json())
    assert response.status_code == 400
    assert response.json() == response_data


def test_delete_role(test_client: TestClient):
    response = test_client.delete(f'/api/v1/role/{5}')
    assert response.status_code == 204

    response = test_client.get('/api/v1/role/')
    assert response.status_code == 200
    assert len(response.json()) == 4


def test_delete_role_invalid_id(test_client: TestClient):
    response_data = roles_data.role_invalid_id_response
    response = test_client.delete(f'/api/v1/role/{999}')
    print('-----', response.json())
    assert response.status_code == 400
    assert response.json() == response_data
