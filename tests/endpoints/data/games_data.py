'''Games data for tests'''


create_game_valid_data = [
    {  # Max data
        'title': 'Game 1',
        'description': 'Description game 1',
        'release': '2015-01-08',
        'developer': 'Developer 1',
        'production': 'Production 1',
        'system_requirements': 'Requirements 1',
        'time_to_play': 10,
        'genres': [],
        'platforms': []
    },
    {  # Min data
        'title': 'Game 2',
        'release': '2015-02-08',
        'genres': [],
        'platforms': []
    },
    {
        'title': 'Game 3',
        'release': '2015-03-08',
        'genres': [],
        'platforms': []
    },
    {
        'title': 'Game 4',
        'release': '2015-04-08',
        'genres': [],
        'platforms': []
    },
    {
        'title': 'Game 5',
        'release': '2015-05-08',
        'genres': [],
        'platforms': []
    }
]

game_valid_data_response = [
    {
        'id': 1,
        'title': 'Game 1', 
        'description': 'Description game 1', 
        'release': '2015-01-08', 
        'developer': 'Developer 1', 
        'production': 'Production 1', 
        'system_requirements': 'Requirements 1', 
        'time_to_play': 10, 
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
        'release': '2015-02-08', 
        'developer': None, 
        'production': None, 
        'system_requirements': None, 
        'time_to_play': 0, 
        'reviews': [], 
        'genres': [], 
        'platforms': [], 
        'comments': [], 
        'grades': []
    },
    {
        'id': 3,
        'title': 'Game 3', 
        'description': None, 
        'release': '2015-03-08', 
        'developer': None, 
        'production': None, 
        'system_requirements': None, 
        'time_to_play': 0, 
        'reviews': [], 
        'genres': [], 
        'platforms': [], 
        'comments': [], 
        'grades': []
    },
    {
        'id': 4,
        'title': 'Game 4', 
        'description': None, 
        'release': '2015-04-08', 
        'developer': None, 
        'production': None, 
        'system_requirements': None, 
        'time_to_play': 0, 
        'reviews': [], 
        'genres': [], 
        'platforms': [], 
        'comments': [], 
        'grades': []
    },
    {
        'id': 5,
        'title': 'Game 5', 
        'description': None, 
        'release': '2015-05-08', 
        'developer': None, 
        'production': None, 
        'system_requirements': None, 
        'time_to_play': 0, 
        'reviews': [], 
        'genres': [], 
        'platforms': [], 
        'comments': [], 
        'grades': []
    }
]

game_nested_response = [
    {
        'id': 1,
        'title': 'Game 1', 
        'description': 'Description game 1', 
        'release': '2015-01-08', 
        'developer': 'Developer 1', 
        'production': 'Production 1', 
        'system_requirements': 'Requirements 1', 
        'time_to_play': 10, 
        'genres': [], 
        'platforms': [], 
    },
    {
        'id': 2,
        'title': 'Game 2', 
        'description': None, 
        'release': '2015-02-08', 
        'developer': None, 
        'production': None, 
        'system_requirements': None, 
        'time_to_play': 0, 
        'genres': [], 
        'platforms': [], 
    },
    {
        'id': 3,
        'title': 'Game 3', 
        'description': None, 
        'release': '2015-03-08', 
        'developer': None, 
        'production': None, 
        'system_requirements': None, 
        'time_to_play': 0, 
        'genres': [], 
        'platforms': [], 
    },
    {
        'id': 4,
        'title': 'Game 4', 
        'description': None, 
        'release': '2015-04-08', 
        'developer': None, 
        'production': None, 
        'system_requirements': None, 
        'time_to_play': 0, 
        'genres': [], 
        'platforms': [], 
    }
]

create_game_invalid_required_data = {'bar': 'baz'}

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

create_game_invalid_release_response = {
    'detail': [
        {
            'loc': ['body', 'release'], 
            'msg': 'invalid date format', 
            'type': 'value_error.date'
        }
    ]
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
    'title': 'Game 5 update',
    'description': 'Description game 5 update',
    'release': '2015-05-05',
    'developer': 'Developer 5 update',
    'production': 'Production 5 update',
    'system_requirements': 'Requirements 5 update',
    'time_to_play': 500,
    'genres': [],
    'platforms': []
}

update_game_valid_data_response = {
    'id': 5,
    'title': 'Game 5 update', 
    'description': 'Description game 5 update', 
    'release': '2015-05-05', 
    'developer': 'Developer 5 update', 
    'production': 'Production 5 update', 
    'system_requirements': 'Requirements 5 update', 
    'time_to_play': 500, 
    'reviews': [], 
    'genres': [], 
    'platforms': [], 
    'comments': [], 
    'grades': []
}

game_invalid_id_response = {
    'detail': 'Game does not exist'
}

upload_game_img_invalid_extension = {
    'detail': 'Image must be with the .png or .jpg or .jpeg extension'
}
