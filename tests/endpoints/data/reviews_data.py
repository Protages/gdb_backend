'''Reviews data for tests'''

from tests.endpoints.data import user_data, games_data


create_review_valid_data = [
    {  # Max data
        'title': 'Review 1',
        'body': 'Review body 1',
        'likes': 10,
        'rating_minus': 5,
        'author': 1,
        'game': 1
    },
    {  # Min data
        'title': 'Review 2',
        'body': 'Review body 2',
        'author': 1,
        'game': 2
    },
    {
        'title': 'Review 3',
        'body': 'Review body 3',
        'author': 2,
        'game': 1
    },
    {
        'title': 'Review 4',
        'body': 'Review body 4',
        'author': 2,
        'game': 2
    },
    {
        'title': 'Review 5',
        'body': 'Review body 5',
        'author': 1,
        'game': 1
    }
]

review_valid_data_response = [
    {
        'id': 1,
        'title': 'Review 1',
        'body': 'Review body 1',
        'likes': 10,
        'rating_minus': 5,
        'author': user_data.user_nested_response[0],
        'game': games_data.game_nested_response[0]
    },
    {
        'id': 2,
        'title': 'Review 2',
        'body': 'Review body 2',
        'likes': 0,
        'rating_minus': 0,
        'author': user_data.user_nested_response[0],
        'game': games_data.game_nested_response[1]
    },
    {
        'id': 3,
        'title': 'Review 3',
        'body': 'Review body 3',
        'likes': 0,
        'rating_minus': 0,
        'author': user_data.user_nested_response[1],
        'game': games_data.game_nested_response[0]
    },
    {
        'id': 4,
        'title': 'Review 4',
        'body': 'Review body 4',
        'likes': 0,
        'rating_minus': 0,
        'author': user_data.user_nested_response[1],
        'game': games_data.game_nested_response[1]
    },
    {
        'id': 5,
        'title': 'Review 5',
        'body': 'Review body 5',
        'likes': 0,
        'rating_minus': 0,
        'author': user_data.user_nested_response[0],
        'game': games_data.game_nested_response[0]
    }
]

create_review_invalid_required_data = {
    'bar': 'baz'  # required title, body, author, game
}

create_review_invalid_required_data_response = {
    'detail': [
        {
            'loc': ['body', 'title'], 
            'msg': 'field required', 
            'type': 'value_error.missing'
        }, 
        {
            'loc': ['body', 'body'], 
            'msg': 'field required', 
            'type': 'value_error.missing'
        }, 
        {
            'loc': ['body', 'author'], 
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

create_review_invalid_user_id = {
    'title': 'Review 999',
    'body': 'Review body 999',
    'author': 999,
    'game': 1
}

create_review_invalid_game_id = {
    'title': 'Review 999',
    'body': 'Review body 999',
    'author': 1,
    'game': 999
}

create_review_invalid_data = {
    'title': 'Review 999',
    'body': 'Review body 999',
    'likes': -1,  # must be >= 0
    'rating_minus': -1,  # must be >= 0
    'author': 1,
    'game': 1
}

create_review_invalid_data_response = {
    'detail': [
        {
            'loc': ['body', 'likes'], 
            'msg': 'ensure this value is greater than or equal to 0.0', 
            'type': 'value_error.number.not_ge', 
            'ctx': {'limit_value': 0.0}
        },
        {
            'loc': ['body', 'rating_minus'], 
            'msg': 'ensure this value is greater than or equal to 0.0', 
            'type': 'value_error.number.not_ge', 
            'ctx': {'limit_value': 0.0}
        }
    ]
}

review_invalid_id_response = {
    'detail': 'Review does not exist'
}

update_review_unused_field = {
    'bar': 'baz'  # we can pass any key-value, it's ok
}

update_review_valid_data = {
    'title': 'Review 5 update',
    'body': 'Review body 5 update',
    'likes': 20,
    'rating_minus': 15
}

update_review_valid_data_response = {
    'id': 5,
    'title': 'Review 5 update',
    'body': 'Review body 5 update',
    'likes': 20,
    'rating_minus': 15,
    'author': user_data.user_nested_response[0],
    'game': games_data.game_nested_response[0]
}

# update_category_invalid_required_data = {
#     'bar': 'baz'  # title required
# }

# update_category_invalid_required_data_response = {
#     'detail': [
#         {
#             'loc': ['body', 'title'], 
#             'msg': 'field required', 
#             'type': 'value_error.missing'
#         }
#     ]
# }

# add_games_to_category_valid_data = {
#     'games': [1, 2, 3, 4]
# }

# add_games_to_category_valid_data_response = {
#     'id': 5,
#     'title': 'Category 5 update',
#     'games': [
#         games_data.game_nested_response[0],
#         games_data.game_nested_response[1],
#         games_data.game_nested_response[2],
#         games_data.game_nested_response[3]
#     ],
#     'user': user_data.user_nested_response[0]
# }

# add_games_to_category_invalid_game_id = {
#     'games': [999]
# }

# remove_games_from_category_valid_data = {
#     'games': [4]
# }

# remove_games_from_category_valid_data_response = {
#     'id': 5,
#     'title': 'Category 5 update',
#     'games': [
#         games_data.game_nested_response[0],
#         games_data.game_nested_response[1],
#         games_data.game_nested_response[2]
#     ],
#     'user': user_data.user_nested_response[0]
# }

# remove_games_from_category_alredy_remove_response = {
#     'detail': 'Game with id 4 are not in category'
# }

# remove_games_from_category_invalid_game_id = {
#     'games': [999]
# }

# remove_all_games_from_category_response = update_category_valid_data_response
