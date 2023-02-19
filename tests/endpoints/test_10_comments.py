# After all these tests, we have comments with id: 1, 2, 3, 4

import pytest

from fastapi.testclient import TestClient

from tests.endpoints.data import comments_data, user_data, games_data, reviews_data


@pytest.mark.order(11)
@pytest.mark.parametrize(
    'request_data, response_data',
    [(a, b) for a, b in zip(
        comments_data.create_comment_valid_data,
        comments_data.comment_valid_data_response
    )]
)
def test_create_comment(test_client: TestClient, request_data, response_data):
    response = test_client.post('/api/v1/comment', json=request_data)
    print('-----', response.json())
    assert response.status_code == 201
    assert response.json() == response_data


def test_create_comment_invalid_required_data(test_client: TestClient):
    request_data = comments_data.create_comment_invalid_required_data
    response_data = comments_data.create_comment_invalid_required_data_response
    response = test_client.post('/api/v1/comment', json=request_data)
    print('-----', response.json())
    assert response.status_code == 422
    assert response.json() == response_data


def test_create_comment_invalid_required_game_review_1(test_client: TestClient):
    request_data = comments_data.create_comment_invalid_required_game_review_1
    response_data = comments_data.create_comment_invalid_required_game_review_1_response
    response = test_client.post('/api/v1/comment', json=request_data)
    print('-----', response.json())
    assert response.status_code == 400
    assert response.json() == response_data


def test_create_comment_invalid_required_game_review_2(test_client: TestClient):
    request_data = comments_data.create_comment_invalid_required_game_review_2
    response_data = comments_data.create_comment_invalid_required_game_review_2_response
    response = test_client.post('/api/v1/comment', json=request_data)
    print('-----', response.json())
    assert response.status_code == 400
    assert response.json() == response_data


def test_create_comment_invalid_user_id(test_client: TestClient):
    request_data = comments_data.create_comment_invalid_user_id
    response_data = user_data.user_invalid_id_response
    response = test_client.post('/api/v1/comment', json=request_data)
    print('-----', response.json())
    assert response.status_code == 400
    assert response.json() == response_data


def test_create_comment_invalid_game_id(test_client: TestClient):
    request_data = comments_data.create_comment_invalid_game_id
    response_data = games_data.game_invalid_id_response
    response = test_client.post('/api/v1/comment', json=request_data)
    print('-----', response.json())
    assert response.status_code == 400
    assert response.json() == response_data


def test_create_comment_invalid_game_id(test_client: TestClient):
    request_data = comments_data.create_comment_invalid_review_id
    response_data = reviews_data.review_invalid_id_response
    response = test_client.post('/api/v1/comment', json=request_data)
    print('-----', response.json())
    assert response.status_code == 400
    assert response.json() == response_data


def test_read_comment(test_client: TestClient):
    response_data = comments_data.comment_valid_data_response[0]
    response = test_client.get(f'/api/v1/comment/{1}')
    print('-----', response.json())
    assert response.status_code == 200
    assert response.json() == response_data


def test_read_comment_invalid_id(test_client: TestClient):
    response_data = comments_data.comment_invalid_id_response
    response = test_client.get(f'/api/v1/comment/{999}')
    print('-----', response.json())
    assert response.status_code == 400
    assert response.json() == response_data


def test_read_all_comment(test_client: TestClient):
    response_data = comments_data.comment_valid_data_response
    response = test_client.get(f'/api/v1/comment/')
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
def test_read_all_comment_invalid_pagination(
        test_client: TestClient, size, page, response_data
    ):
    response = test_client.get(f'/api/v1/comment/?size={size}&page={page}')
    print('-----', response.json())
    assert response.status_code == 400
    assert response.json() == response_data


def test_update_comment(test_client: TestClient):
    request_data = comments_data.update_comment_valid_data
    response_data = comments_data.update_comment_valid_data_response
    response = test_client.put(f'/api/v1/comment/{5}', json=request_data)
    print('-----', response.json())
    assert response.status_code == 200
    assert response.json() == response_data


def test_update_comment_invalid_data(test_client: TestClient):
    request_data = comments_data.update_comment_invalid_data
    response_data = comments_data.update_comment_invalid_data_response
    response = test_client.put(f'/api/v1/comment/{5}', json=request_data)
    print('-----', response.json())
    assert response.status_code == 422
    assert response.json() == response_data


def test_update_comment_invalid_id(test_client: TestClient):
    request_data = comments_data.update_comment_valid_data
    response_data = comments_data.comment_invalid_id_response
    response = test_client.put(f'/api/v1/comment/{999}', json=request_data)
    print('-----', response.json())
    assert response.status_code == 400
    assert response.json() == response_data


def test_delete_comment(test_client: TestClient):
    response = test_client.delete(f'/api/v1/comment/{5}')
    assert response.status_code == 204

    response = test_client.get(f'/api/v1/comment/')
    assert response.status_code == 200
    assert len(response.json()) == 4


def test_delete_comment_invalid_id(test_client: TestClient):
    response_data = comments_data.comment_invalid_id_response
    response = test_client.delete(f'/api/v1/comment/{999}')
    print('-----', response.json())
    assert response.status_code == 400
    assert response.json() == response_data
