# After all these tests, we have genres with id: 1, 2, 3, 4

import pytest

from fastapi.testclient import TestClient

from tests.endpoints.data import genres_data


@pytest.mark.order(4)
@pytest.mark.parametrize(
    'request_data, response_data',
    [(a, b) for a, b in zip(
        genres_data.create_genre_valid_data, genres_data.genre_valid_data_response
    )]
)
def test_create_genre(test_client: TestClient, request_data, response_data):
    response = test_client.post('/api/v1/genre', json=request_data)
    print('-----', response.json())
    assert response.status_code == 201
    assert response.json() == response_data


def test_create_genre_invalid_data(test_client: TestClient):
    request_data = genres_data.create_genre_invalid_data
    response_data = genres_data.create_genre_invalid_data_response
    response = test_client.post('/api/v1/genre', json=request_data)
    print('-----', response.json())
    assert response.status_code == 422
    assert response.json() == response_data


def test_read_genre(test_client: TestClient):
    response_data = genres_data.genre_valid_data_response[0]
    response = test_client.get(f'/api/v1/genre/{1}')
    print('-----', response.json())
    assert response.status_code == 200
    assert response.json() == response_data


def test_read_genre_invalid_id(test_client: TestClient):
    response_data = genres_data.genre_invalid_id_response
    response = test_client.get(f'/api/v1/genre/{999}')
    print('-----', response.json())
    assert response.status_code == 400
    assert response.json() == response_data


def test_read_all_genre(test_client: TestClient):
    response_data = genres_data.genre_valid_data_response
    response = test_client.get('/api/v1/genre/')
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
def test_read_all_genre_invalid_pagination(
    test_client: TestClient, size, page, response_data
):
    response = test_client.get(f'/api/v1/genre/?size={size}&page={page}')
    print('-----', response.json())
    assert response.status_code == 400
    assert response.json() == response_data


def test_update_genre(test_client: TestClient):
    request_data = genres_data.update_genre_valid_data
    response_data = genres_data.update_genre_valid_data_response
    response = test_client.put(f'/api/v1/genre/{5}', json=request_data)
    print('-----', response.json())
    assert response.status_code == 200
    assert response.json() == response_data


def test_update_genre_invalid_id(test_client: TestClient):
    request_data = genres_data.update_genre_valid_data
    response_data = genres_data.genre_invalid_id_response
    response = test_client.put(f'/api/v1/genre/{999}', json=request_data)
    print('-----', response.json())
    assert response.status_code == 400
    assert response.json() == response_data


def test_update_genre_invalid_data(test_client: TestClient):
    request_data = genres_data.create_genre_invalid_data
    response_data = genres_data.create_genre_invalid_data_response
    response = test_client.put(f'/api/v1/genre/{1}', json=request_data)
    print('-----', response.json())
    assert response.status_code == 422
    assert response.json() == response_data


def test_delete_genre(test_client: TestClient):
    response = test_client.delete(f'/api/v1/genre/{5}')
    assert response.status_code == 204

    response = test_client.get('/api/v1/genre/')
    assert response.status_code == 200
    assert len(response.json()) == 4


def test_delete_genre_invalid_id(test_client: TestClient):
    response_data = genres_data.genre_invalid_id_response
    response = test_client.delete(f'/api/v1/genre/{999}')
    print('-----', response.json())
    assert response.status_code == 400
    assert response.json() == response_data
