# After all these tests, we have games with id: 1, 2, 3, 4

import pytest

from fastapi.testclient import TestClient

from tests.endpoints.data import games_data, genres_data, platforms_data


@pytest.mark.order(6)
@pytest.mark.parametrize(
    'request_data, response_data',
    [(a, b) for a, b in zip(
        games_data.create_game_valid_data, games_data.game_valid_data_response
    )]
)
def test_create_game(test_client: TestClient, request_data, response_data):
    response = test_client.post('/api/v1/game', json=request_data)
    print('-----', response.json())
    assert response.status_code == 201
    assert response.json() == response_data


def test_create_game_invalid_required_data(test_client: TestClient):
    request_data = games_data.create_game_invalid_required_data
    response_data = games_data.create_game_invalid_required_data_response
    response = test_client.post('/api/v1/game', json=request_data)
    print('-----', response.json())
    assert response.status_code == 422
    assert response.json() == response_data


def test_create_game_invalid_release(test_client: TestClient):
    request_data = games_data.create_game_invalid_release
    response_data = games_data.create_game_invalid_release_response
    response = test_client.post('/api/v1/game', json=request_data)
    print('-----', response.json())
    assert response.status_code == 422
    assert response.json() == response_data


def test_create_game_invalid_genres_id(test_client: TestClient):
    request_data = games_data.create_game_invalid_genres_id
    response_data = genres_data.genre_invalid_id_response
    response = test_client.post('/api/v1/game', json=request_data)
    print('-----', response.json())
    assert response.status_code == 400
    assert response.json() == response_data


def test_create_game_invalid_platforms_id(test_client: TestClient):
    request_data = games_data.create_game_invalid_platforms_id
    response_data = platforms_data.platform_invalid_id_response
    response = test_client.post('/api/v1/game', json=request_data)
    print('-----', response.json())
    assert response.status_code == 400
    assert response.json() == response_data


def test_read_game(test_client: TestClient):
    response_data = games_data.game_valid_data_response[0]
    response = test_client.get(f'/api/v1/game/{1}')
    print('-----', response.json())
    assert response.status_code == 200
    assert response.json() == response_data


def test_read_game_invalid_id(test_client: TestClient):
    response_data = games_data.game_invalid_id_response
    response = test_client.get(f'/api/v1/game/{999}')
    print('-----', response.json())
    assert response.status_code == 400
    assert response.json() == response_data


def test_read_all_game(test_client: TestClient):
    response_data = games_data.game_valid_data_response
    response = test_client.get('/api/v1/game/')
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
def test_read_all_game_invalid_pagination(
    test_client: TestClient, size, page, response_data
):
    response = test_client.get(f'/api/v1/game/?size={size}&page={page}')
    print('-----', response.json())
    assert response.status_code == 400
    assert response.json() == response_data


def test_update_game_unused_field(test_client: TestClient):
    request_data = {
        'bar': 'baz'  # We can send any key-value, it's ok
    }
    response_data = games_data.game_valid_data_response[4]
    response = test_client.put(f'/api/v1/game/{5}', json=request_data)
    print('-----', response.json())
    assert response.status_code == 200
    assert response.json() == response_data


def test_update_game(test_client: TestClient):
    request_data = games_data.update_game_valid_data
    response_data = games_data.update_game_valid_data_response
    response = test_client.put(f'/api/v1/game/{5}', json=request_data)
    print('-----', response.json())
    assert response.status_code == 200
    assert response.json() == response_data


def test_update_update_invalid_id(test_client: TestClient):
    request_data = games_data.update_game_valid_data
    response_data = games_data.game_invalid_id_response
    response = test_client.put(f'/api/v1/game/{999}', json=request_data)
    print('-----', response.json())
    assert response.status_code == 400
    assert response.json() == response_data


def test_delete_game(test_client: TestClient):
    response = test_client.delete(f'/api/v1/game/{5}')
    assert response.status_code == 204

    response = test_client.get('/api/v1/game/')
    assert response.status_code == 200
    assert len(response.json()) == 4


def test_delete_game_invalid_id(test_client: TestClient):
    response_data = games_data.game_invalid_id_response
    response = test_client.delete(f'/api/v1/game/{999}')
    print('-----', response.json())
    assert response.status_code == 400
    assert response.json() == response_data
