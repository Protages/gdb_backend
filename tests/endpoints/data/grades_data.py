'''Grades data for tests'''

from tests.endpoints.data import user_data, games_data 


create_grade_valid_data = [
    {
        'score': 1,
        'user': 1,
        'game': 1
    },
    {
        'score': 2,
        'user': 1,
        'game': 2
    },
    {
        'score': 3,
        'user': 1,
        'game': 3
    },
    {
        'score': 4,
        'user': 1,
        'game': 4
    },
    {
        'score': 5,
        'user': 2,
        'game': 1
    }
]

grade_valid_data_response = [
    {
        'id': 1,
        'score': 1,
        'user': user_data.user_nested_response[0],
        'game': games_data.game_nested_response[0]
    },
    {
        'id': 2,
        'score': 2,
        'user': user_data.user_nested_response[0],
        'game': games_data.game_nested_response[1]
    },
    {
        'id': 3,
        'score': 3,
        'user': user_data.user_nested_response[0],
        'game': games_data.game_nested_response[2]
    },
    {
        'id': 4,
        'score': 4,
        'user': user_data.user_nested_response[0],
        'game': games_data.game_nested_response[3]
    },
    {
        'id': 5,
        'score': 5,
        'user': user_data.user_nested_response[1],
        'game': games_data.game_nested_response[0]
    }
]

create_grade_invalid_data = {
    'bar': 'baz'  # required score, user, game
}

create_grade_invalid_data_response = {
    'detail': [
        {
            'loc': ['body', 'score'], 
            'msg': 'field required', 
            'type': 'value_error.missing'
        }, 
        {
            'loc': ['body', 'user'], 
            'msg': 'field required', 
            'type': 'value_error.missing'
        }, 
        {
            'loc': ['body', 'game'], 
            'msg': 'field required', 
            'type': 'value_error.missing'
        }
    ]
}

create_grade_invalid_score = [
    {
        'score': 0,  # valid 1 <= score <= 10
        'user': 4,
        'game': 4
    },
    {
        'score': 11,  # valid 1 <= score <= 10
        'user': 4,
        'game': 4
    }
]

create_grade_invalid_score_response = {
    'detail': [
        {
            'loc': ['body', 'score'], 
            'msg': 'Score is not valid, must be from 1 to 10', 
            'type': 'value_error'
        }
    ]
}

create_grade_invalid_user_id = {
    'score': 10,
    'user': 999,  # invalid
    'game': 4
}

create_grade_invalid_game_id = {
    'score': 10,
    'user': 4,
    'game': 999  # invalid
}

grade_invalid_id_response = {
    'detail': 'Grade does not exist'
}

update_grade_valid_data = {
    'score': 10
}

update_grade_valid_data_response = {
    'id': 5,
    'score': 10,
    'user': user_data.user_nested_response[1],
    'game': games_data.game_nested_response[0]
}

update_grade_invalid_data = {
    'bar': 'baz'  # required score
}

update_grade_invalid_data_response = {
    'detail': [
        {
            'loc': ['body', 'score'], 
            'msg': 'field required', 
            'type': 'value_error.missing'
        }
    ]
}
