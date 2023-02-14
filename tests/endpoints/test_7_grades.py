# After all these tests, we have grades with id: 1, 2, 3, 4

import pytest

from fastapi.testclient import TestClient

from tests.endpoints.data import grades_data, user_data, games_data


@pytest.mark.parametrize(
    'request_data, response_data',
    [(a, b) for a, b in zip(
        grades_data.create_grade_valid_data, grades_data.grade_valid_data_response
    )]
)
def test_create_grade(test_client: TestClient, request_data, response_data):
    response = test_client.post('/api/v1/grade', json=request_data)
    print('-----', response.json())
    assert response.status_code == 201
    assert response.json() == response_data


def test_create_grade_invalid_data(test_client: TestClient):
    request_data = grades_data.create_grade_invalid_data
    response_data = grades_data.create_grade_invalid_data_response
    response = test_client.post('/api/v1/grade', json=request_data)
    print('-----', response.json())
    assert response.status_code == 422
    assert response.json() == response_data


@pytest.mark.parametrize(
    'response_data', [grades_data.create_grade_invalid_score_response]
)
@pytest.mark.parametrize('request_data', grades_data.create_grade_invalid_score)
def test_create_grade_invalid_score(
        test_client: TestClient, request_data, response_data
    ):
    response = test_client.post('/api/v1/grade', json=request_data)
    print('-----', response.json())
    assert response.status_code == 422
    assert response.json() == response_data


def test_create_grade_invalid_user_id(test_client: TestClient):
    request_data = grades_data.create_grade_invalid_user_id
    response_data = user_data.user_invalid_id_response
    response = test_client.post('/api/v1/grade', json=request_data)
    print('-----', response.json())
    assert response.status_code == 400
    assert response.json() == response_data


def test_create_grade_invalid_game_id(test_client: TestClient):
    request_data = grades_data.create_grade_invalid_game_id
    response_data = games_data.game_invalid_id_response
    response = test_client.post('/api/v1/grade', json=request_data)
    print('-----', response.json())
    assert response.status_code == 400
    assert response.json() == response_data


def test_read_grade(test_client: TestClient):
    response_data = grades_data.grade_valid_data_response[0]
    response = test_client.get(f'/api/v1/grade/{1}')
    print('-----', response.json())
    assert response.status_code == 200
    assert response.json() == response_data


def test_read_grade_invalid_id(test_client: TestClient):
    response_data = grades_data.grade_invalid_id_response
    response = test_client.get(f'/api/v1/grade/{999}')
    print('-----', response.json())
    assert response.status_code == 400
    assert response.json() == response_data


def test_read_all_grade(test_client: TestClient):
    response_data = grades_data.grade_valid_data_response
    response = test_client.get(f'/api/v1/grade/')
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
def test_read_all_grade_invalid_pagination(
        test_client: TestClient, size, page, response_data
    ):
    response = test_client.get(f'/api/v1/grade/?size={size}&page={page}')
    print('-----', response.json())
    assert response.status_code == 400
    assert response.json() == response_data


def test_update_grade(test_client: TestClient):
    request_data = grades_data.update_grade_valid_data
    response_data = grades_data.update_grade_valid_data_response
    response = test_client.put(f'/api/v1/grade/{5}', json=request_data)
    print('-----', response.json())
    assert response.status_code == 200
    assert response.json() == response_data


def test_update_grade_invalid_data(test_client: TestClient):
    request_data = grades_data.update_grade_invalid_data
    response_data = grades_data.update_grade_invalid_data_response
    response = test_client.put(f'/api/v1/grade/{5}', json=request_data)
    print('-----', response.json())
    assert response.status_code == 422
    assert response.json() == response_data


@pytest.mark.parametrize(
    'response_data', [grades_data.create_grade_invalid_score_response]
)
@pytest.mark.parametrize('request_data', grades_data.create_grade_invalid_score)
def test_update_grade_invalid_score(
        test_client: TestClient, response_data, request_data
    ):
    response = test_client.put(f'/api/v1/grade/{5}', json=request_data)
    print('-----', response.json())
    assert response.status_code == 422
    assert response.json() == response_data


def test_update_grade_invalid_id(test_client: TestClient):
    request_data = grades_data.update_grade_valid_data
    response_data = grades_data.grade_invalid_id_response
    response = test_client.put(f'/api/v1/grade/{999}', json=request_data)
    print('-----', response.json())
    assert response.status_code == 400
    assert response.json() == response_data


def test_delete_grade(test_client: TestClient):
    response = test_client.delete(f'/api/v1/grade/{5}')
    assert response.status_code == 204

    response = test_client.get(f'/api/v1/grade/')
    assert response.status_code == 200
    assert len(response.json()) == 4


def test_delete_grade_invalid_id(test_client: TestClient):
    response_data = grades_data.grade_invalid_id_response
    response = test_client.delete(f'/api/v1/grade/{999}')
    print('-----', response.json())
    assert response.status_code == 400
    assert response.json() == response_data
