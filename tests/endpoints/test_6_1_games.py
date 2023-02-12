# After all these tests, we have games with id: 1

import pytest

from fastapi.testclient import TestClient

create_game_valid_data = [
    {  # Max data
        'title': 'Game 1',
        'description': 'Description game 1',
        'release': '2023-02-08',
        'developer': 'Developer 1',
        'production': 'Production 1',
        'system_requirements': 'Requirements 1',
        'time_to_play': 10,
        'genres': [],
        'platforms': []
    },
    {  # Min data
        'title': 'Game 2',
        'release': '2023-02-08',
        'genres': [],
        'platforms': []
    }
]

create_game_valid_data_response = [
    {
        'id': 1,
        'title': 'Game 1', 
        'description': 'Description game 1', 
        'release': '2023-02-08', 
        'developer': 'Developer 1', 
        'production': 'Production 1', 
        'system_requirements': 'Requirements 1', 
        'time_to_play': 10, 
        'main_image_path': 'src\\static_test\\img\\games\\default.png', 
        'reviews': [], 
        'genres': [], 
        'platforms': [], 
        'comments': [], 
        'grades': []
    },
    {
        'id': 2,
        'title': 'Game 2', 
        'description': None, 
        'release': '2023-02-08', 
        'developer': None, 
        'production': None, 
        'system_requirements': None, 
        'time_to_play': 0, 
        'main_image_path': 'src\\static_test\\img\\games\\default.png', 
        'reviews': [], 
        'genres': [], 
        'platforms': [], 
        'comments': [], 
        'grades': []
    }
]

create_game_invalid_required_data_response = {
    'detail': [
        {
            "loc": ["body", "title"],
            "msg": "field required",
            "type": "value_error.missing"
        },
        {
            "loc": ["body", "release"],
            "msg": "field required",
            "type": "value_error.missing"
        },
        {
            "loc": ["body", "genres"],
            "msg": "field required",
            "type": "value_error.missing"
        },
        {
            "loc": ["body", "platforms"],
            "msg": "field required",
            "type": "value_error.missing"
        }
    ]
}

create_game_invalid_release = {
    'title': 'Game 3',
    'release': '08.12.2020',
    'genres': [],
    'platforms': []
}

create_game_invalid_genres_id = {
    'title': 'Game 3',
    'release': '2023-02-08',
    'genres': [999, 1000],
    'platforms': []
}

create_game_invalid_platforms_id = {
    'title': 'Game 3',
    'release': '2023-02-08',
    'genres': [],
    'platforms': [999, 1000]
}

update_game_valid_data = {
    'title': 'Game 1 update',
    'description': 'Description game 1 update',
    'release': '2022-02-08',
    'developer': 'Developer 1 update',
    'production': 'Production 1 update',
    'system_requirements': 'Requirements 1 update',
    'time_to_play': 100,
    'genres': [],
    'platforms': []
}

update_game_valid_data_response = {
    'id': 1,
    'title': 'Game 1 update', 
    'description': 'Description game 1 update', 
    'release': '2022-02-08', 
    'developer': 'Developer 1 update', 
    'production': 'Production 1 update', 
    'system_requirements': 'Requirements 1 update', 
    'time_to_play': 100, 
    'main_image_path': 'src\\static_test\\img\\games\\default.png', 
    'reviews': [], 
    'genres': [], 
    'platforms': [], 
    'comments': [], 
    'grades': []
}


@pytest.mark.parametrize(
    'request_data, response_data',
    [
        (create_game_valid_data[0], create_game_valid_data_response[0]),
        (create_game_valid_data[1], create_game_valid_data_response[1])
    ]
)
def test_create_game(test_client: TestClient, request_data, response_data):
    response = test_client.post('/api/v1/game', json=request_data)
    print('-----', response.json())
    assert response.status_code == 201
    assert response.json() == response_data


def test_create_game_invalid_required_data(test_client: TestClient):
    request_data = {'bar': 'baz'}
    response_data = create_game_invalid_required_data_response
    response = test_client.post('/api/v1/game', json=request_data)
    print('-----', response.json())
    assert response.status_code == 422
    assert response.json() == response_data


def test_create_game_invalid_release(test_client: TestClient):
    request_data = create_game_invalid_release
    response_data = {
        'detail': [
            {
                'loc': ['body', 'release'], 
                'msg': 'invalid date format', 
                'type': 'value_error.date'
            }
        ]
    }
    response = test_client.post('/api/v1/game', json=request_data)
    print('-----', response.json())
    assert response.status_code == 422
    assert response.json() == response_data


def test_create_game_invalid_genres_id(test_client: TestClient):
    request_data = create_game_invalid_genres_id
    response_data = {'detail': 'Genre does not exist'}
    response = test_client.post('/api/v1/game', json=request_data)
    print('-----', response.json())
    assert response.status_code == 400
    assert response.json() == response_data


def test_create_game_invalid_platforms_id(test_client: TestClient):
    request_data = create_game_invalid_platforms_id
    response_data = {'detail': 'Platform does not exist'}
    response = test_client.post('/api/v1/game', json=request_data)
    print('-----', response.json())
    assert response.status_code == 400
    assert response.json() == response_data


def test_read_game(test_client: TestClient):
    response_data = create_game_valid_data_response[0]
    response = test_client.get(f'/api/v1/game/{1}')
    print('-----', response.json())
    assert response.status_code == 200
    assert response.json() == response_data


def test_read_game_invalid_id(test_client: TestClient):
    response_data = {'detail': 'Game does not exist'}
    response = test_client.get(f'/api/v1/game/{999}')
    print('-----', response.json())
    assert response.status_code == 400
    assert response.json() == response_data


def test_read_all_game(test_client: TestClient):
    response_data = create_game_valid_data_response
    response = test_client.get(f'/api/v1/game/all/')
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
    response = test_client.get(f'/api/v1/game/all/?size={size}&page={page}')
    print('-----', response.json())
    assert response.status_code == 400
    assert response.json() == response_data


def test_update_game_unused_field(test_client: TestClient):
    request_data = {
        'bar': 'baz'  # We can send any key-value, it's ok
    }
    response_data = create_game_valid_data_response[0]
    response = test_client.put(f'/api/v1/game/{1}', json=request_data)
    print('-----', response.json())
    assert response.status_code == 200
    assert response.json() == response_data


def test_update_game(test_client: TestClient):
    request_data = update_game_valid_data
    response_data = update_game_valid_data_response
    response = test_client.put(f'/api/v1/game/{1}', json=request_data)
    print('-----', response.json())
    assert response.status_code == 200
    assert response.json() == response_data


def test_update_update_invalid_id(test_client: TestClient):
    request_data = {'title': 'Game 999 update'}
    response_data = {'detail': 'Game does not exist'}
    response = test_client.put(f'/api/v1/game/{999}', json=request_data)
    print('-----', response.json())
    assert response.status_code == 400
    assert response.json() == response_data


def test_delete_game(test_client: TestClient):
    response = test_client.delete(f'/api/v1/game/{2}')
    assert response.status_code == 204


def test_delete_game_invalid_id(test_client: TestClient):
    response_data = {
        'detail': 'Game does not exist'
    }
    response = test_client.delete(f'/api/v1/game/{999}')
    print('-----', response.json())
    assert response.status_code == 400
    assert response.json() == response_data
