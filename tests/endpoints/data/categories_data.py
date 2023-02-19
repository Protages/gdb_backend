'''Categories data for tests'''

from tests.endpoints.data import user_data, games_data


create_category_valid_data = [
    {
        'title': 'Category 1',
        'user': 1
    },
    {
        'title': 'Category 2',
        'user': 1
    },
    {
        'title': 'Category 3',
        'user': 1
    },
    {
        'title': 'Category 4',
        'user': 1
    },
    {
        'title': 'Category 5',
        'user': 1
    },
]

category_valid_data_response = [
    {
        'id': 1,
        'title': 'Category 1',
        'games': [],
        'user': user_data.user_nested_response[0]
    },
    {
        'id': 2,
        'title': 'Category 2',
        'games': [],
        'user': user_data.user_nested_response[0]
    },
    {
        'id': 3,
        'title': 'Category 3',
        'games': [],
        'user': user_data.user_nested_response[0]
    },
    {
        'id': 4,
        'title': 'Category 4',
        'games': [],
        'user': user_data.user_nested_response[0]
    },
    {
        'id': 5,
        'title': 'Category 5',
        'games': [],
        'user': user_data.user_nested_response[0]
    },
]

create_category_invalid_required_data = {
    'bar': 'baz'  # required title, user
}

create_category_invalid_required_data_response = {
    'detail': [
        {
            'loc': ['body', 'title'],
            'msg': 'field required',
            'type': 'value_error.missing'
        },
        {
            'loc': ['body', 'user'],
            'msg': 'field required',
            'type': 'value_error.missing'
        }
    ]
}

create_category_invalid_user_id = {
    'title': 'Category 999',
    'user': 999
}

create_category_invalid_game_id = {
    'title': 'Category 999',
    'user': 1,
    'games': [999, 1000]
}

create_category_invalid_unique = {
    'title': 'Category 1',  # unique_together for title and user
    'user': 1
}

category_invalid_unique_response = {
    'detail': 'title and user field must be unique together'
}

category_invalid_id_response = {
    'detail': 'Category does not exist'
}

update_category_valid_data = {
    'title': 'Category 5 update'
}

update_category_valid_data_response = {
    'id': 5,
    'title': 'Category 5 update',
    'games': [],
    'user': user_data.user_nested_response[0]
}

update_category_invalid_unique = {
    'title': 'Category 1',
}

update_category_invalid_required_data = {
    'bar': 'baz'  # title required
}

update_category_invalid_required_data_response = {
    'detail': [
        {
            'loc': ['body', 'title'],
            'msg': 'field required',
            'type': 'value_error.missing'
        }
    ]
}

add_games_to_category_valid_data = {
    'games': [1, 2, 3, 4]
}

add_games_to_category_valid_data_response = {
    'id': 5,
    'title': 'Category 5 update',
    'games': [
        games_data.game_nested_response[0],
        games_data.game_nested_response[1],
        games_data.game_nested_response[2],
        games_data.game_nested_response[3]
    ],
    'user': user_data.user_nested_response[0]
}

add_games_to_category_invalid_game_id = {
    'games': [999]
}

remove_games_from_category_valid_data = {
    'games': [4]
}

remove_games_from_category_valid_data_response = {
    'id': 5,
    'title': 'Category 5 update',
    'games': [
        games_data.game_nested_response[0],
        games_data.game_nested_response[1],
        games_data.game_nested_response[2]
    ],
    'user': user_data.user_nested_response[0]
}

remove_games_from_category_alredy_remove_response = {
    'detail': 'Game with id 4 are not in category'
}

remove_games_from_category_invalid_game_id = {
    'games': [999]
}

remove_all_games_from_category_response = update_category_valid_data_response
