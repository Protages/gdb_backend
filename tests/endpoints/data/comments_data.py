'''Comments data for tests'''

from tests.endpoints.data import user_data, games_data


create_comment_valid_data = [
    {
        'body': 'Comment 1',
        'user': 1,
        'game': 1
    },
    {
        'body': 'Comment 2',
        'user': 1,
        'game': 2
    },
    {
        'body': 'Comment 3',
        'user': 2,
        'game': 1
    },
    {
        'body': 'Comment 4',
        'user': 2,
        'game': 2
    },
    {
        'body': 'Comment 5',
        'user': 1,
        'game': 1
    }
]

comment_valid_data_response = [
    {
        'id': 1,
        'body': 'Comment 1',
        'user': user_data.user_nested_response[0],
        'game': games_data.game_nested_response[0],
        'review': None
    },
    {
        'id': 2,
        'body': 'Comment 2',
        'user': user_data.user_nested_response[0],
        'game': games_data.game_nested_response[1],
        'review': None
    },
    {
        'id': 3,
        'body': 'Comment 3',
        'user': user_data.user_nested_response[1],
        'game': games_data.game_nested_response[0],
        'review': None
    },
    {
        'id': 4,
        'body': 'Comment 4',
        'user': user_data.user_nested_response[1],
        'game': games_data.game_nested_response[1],
        'review': None
    },
    {
        'id': 5,
        'body': 'Comment 5',
        'user': user_data.user_nested_response[0],
        'game': games_data.game_nested_response[0],
        'review': None
    }
]

create_comment_invalid_required_data = {
    'bar': 'baz'  # required body, user
}

create_comment_invalid_required_data_response = {
    'detail': [
        {
            'loc': ['body', 'body'], 
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

create_comment_invalid_required_game_review_1 = {
    'body': 'Comment 999',  # required game or review
    'user': 1
}

create_comment_invalid_required_game_review_1_response = {
    'detail': 'Need to pass game ID or review ID'
}

create_comment_invalid_required_game_review_2 = {
    'body': 'Comment 999',  
    'user': 1,
    'game': 1,  # required game or review, not together
    'review': 1
}

create_comment_invalid_required_game_review_2_response = {
    'detail': 'Pass game ID or review ID, not together'
}

create_comment_invalid_user_id = {
    'body': 'Comment 999',  
    'user': 999,
    'game': 1
}

create_comment_invalid_game_id = {
    'body': 'Comment 999',  
    'user': 1,
    'game': 999
}

create_comment_invalid_review_id = {
    'body': 'Comment 999',  
    'user': 1,
    'review': 999
}

comment_invalid_id_response = {
    'detail': 'Comment does not exist'
}

update_comment_valid_data = {
    'body': 'Comment 5 update',
}

update_comment_valid_data_response = {
    'id': 5,
    'body': 'Comment 5 update',
    'user': user_data.user_nested_response[0],
    'game': games_data.game_nested_response[0],
    'review': None
}

update_comment_invalid_data = {
    'bar': 'baz'  # required body
}

update_comment_invalid_data_response = {
    'detail': [
        {
            'loc': ['body', 'body'], 
            'msg': 'field required', 
            'type': 'value_error.missing'
        }
    ]
}
