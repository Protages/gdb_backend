# After all these tests, we have categories with id: 1, 2, 3, 4

import pytest

from fastapi.testclient import TestClient

from tests.endpoints.data import categories_data, user_data, games_data


@pytest.mark.order(9)
@pytest.mark.parametrize(
    'request_data, response_data',
    [(a, b) for a, b in zip(
        categories_data.create_category_valid_data,
        categories_data.category_valid_data_response
    )]
)
def test_create_category(test_client: TestClient, request_data, response_data):
    response = test_client.post('/api/v1/category', json=request_data)
    print('-----', response.json())
    assert response.status_code == 201
    assert response.json() == response_data


def test_create_category_invalid_required_data(test_client: TestClient):
    request_data = categories_data.create_category_invalid_required_data
    response_data = categories_data.create_category_invalid_required_data_response
    response = test_client.post('/api/v1/category', json=request_data)
    print('-----', response.json())
    assert response.status_code == 422
    assert response.json() == response_data


def test_create_category_invalid_user_id(test_client: TestClient):
    request_data = categories_data.create_category_invalid_user_id
    response_data = user_data.user_invalid_id_response
    response = test_client.post('/api/v1/category', json=request_data)
    print('-----', response.json())
    assert response.status_code == 400
    assert response.json() == response_data


def test_create_category_invalid_game_id(test_client: TestClient):
    request_data = categories_data.create_category_invalid_game_id
    response_data = games_data.game_invalid_id_response
    response = test_client.post('/api/v1/category', json=request_data)
    print('-----', response.json())
    assert response.status_code == 400
    assert response.json() == response_data


def test_create_category_invalid_unique(test_client: TestClient):
    request_data = categories_data.create_category_invalid_unique
    response_data = categories_data.category_invalid_unique_response
    response = test_client.post('/api/v1/category', json=request_data)
    print('-----', response.json())
    assert response.status_code == 400
    assert response.json() == response_data


def test_read_category(test_client: TestClient):
    response_data = categories_data.category_valid_data_response[0]
    response = test_client.get(f'/api/v1/category/{1}')
    print('-----', response.json())
    assert response.status_code == 200
    assert response.json() == response_data


def test_read_category_invalid_id(test_client: TestClient):
    response_data = categories_data.category_invalid_id_response
    response = test_client.get(f'/api/v1/category/{999}')
    print('-----', response.json())
    assert response.status_code == 400
    assert response.json() == response_data


def test_read_all_category(test_client: TestClient):
    response_data = categories_data.category_valid_data_response
    response = test_client.get(f'/api/v1/category/')
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
def test_read_all_category_invalid_pagination(
        test_client: TestClient, size, page, response_data
    ):
    response = test_client.get(f'/api/v1/category/?size={size}&page={page}')
    print('-----', response.json())
    assert response.status_code == 400
    assert response.json() == response_data


def test_update_category(test_client: TestClient):
    request_data = categories_data.update_category_valid_data
    response_data = categories_data.update_category_valid_data_response
    response = test_client.put(f'/api/v1/category/{5}', json=request_data)
    print('-----', response.json())
    assert response.status_code == 200
    assert response.json() == response_data


def test_update_category_invalid_unique(test_client: TestClient):
    request_data = categories_data.update_category_invalid_unique
    response_data = categories_data.category_invalid_unique_response
    response = test_client.put(f'/api/v1/category/{5}', json=request_data)
    print('-----', response.json())
    assert response.status_code == 400
    assert response.json() == response_data


def test_update_category_invalid_required(test_client: TestClient):
    request_data = categories_data.update_category_invalid_required_data
    response_data = categories_data.update_category_invalid_required_data_response
    response = test_client.put(f'/api/v1/category/{5}', json=request_data)
    print('-----', response.json())
    assert response.status_code == 422
    assert response.json() == response_data


def test_update_category_invalid_id(test_client: TestClient):
    request_data = categories_data.update_category_valid_data
    response_data = categories_data.category_invalid_id_response
    response = test_client.put(f'/api/v1/category/{999}', json=request_data)
    print('-----', response.json())
    assert response.status_code == 400
    assert response.json() == response_data


def test_add_games_to_category(test_client: TestClient):
    request_data = categories_data.add_games_to_category_valid_data
    response_data = categories_data.add_games_to_category_valid_data_response
    response = test_client.post(f'/api/v1/category/{5}/games', json=request_data)
    print('-----', response.json())
    assert response.status_code == 200
    assert response.json() == response_data


def test_add_games_to_category_invalid_game_id(test_client: TestClient):
    request_data = categories_data.add_games_to_category_invalid_game_id
    response_data = games_data.game_invalid_id_response
    response = test_client.post(f'/api/v1/category/{5}/games', json=request_data)
    print('-----', response.json())
    assert response.status_code == 400
    assert response.json() == response_data


def test_remove_games_from_category(test_client: TestClient):
    request_data = categories_data.remove_games_from_category_valid_data
    response_data = categories_data.remove_games_from_category_valid_data_response
    response = test_client.put(f'/api/v1/category/{5}/games', json=request_data)
    print('-----', response.json())
    assert response.status_code == 200
    assert response.json() == response_data


def test_remove_games_from_category_alredy_remove(test_client: TestClient):
    request_data = categories_data.remove_games_from_category_valid_data
    response_data = categories_data.remove_games_from_category_alredy_remove_response
    response = test_client.put(f'/api/v1/category/{5}/games', json=request_data)
    print('-----', response.json())
    assert response.status_code == 400
    assert response.json() == response_data


def test_remove_games_from_category_invalid_game_id(test_client: TestClient):
    request_data = categories_data.remove_games_from_category_invalid_game_id
    response_data = games_data.game_invalid_id_response
    response = test_client.put(f'/api/v1/category/{5}/games', json=request_data)
    print('-----', response.json())
    assert response.status_code == 400
    assert response.json() == response_data


def test_remove_all_games_from_category(test_client: TestClient):
    response_data = categories_data.remove_all_games_from_category_response
    response = test_client.delete(f'/api/v1/category/{5}/games')
    print('-----', response.json())
    assert response.status_code == 200
    assert response.json() == response_data


def test_delete_category(test_client: TestClient):
    response = test_client.delete(f'/api/v1/category/{5}')
    assert response.status_code == 204

    response = test_client.get(f'/api/v1/category/')
    assert response.status_code == 200
    assert len(response.json()) == 4


def test_delete_category_invalid_id(test_client: TestClient):
    response_data = categories_data.category_invalid_id_response
    response = test_client.delete(f'/api/v1/category/{999}')
    print('-----', response.json())
    assert response.status_code == 400
    assert response.json() == response_data
