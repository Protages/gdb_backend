'''Users data for tests'''


create_user_valid_data = [
    {  # Max data
        'email': 'user.1@gmail.com',
        'about': 'About user 1',
        'rating': 1,
        'is_active': False,
        'is_superuser': True,
        'username': 'User_1',
        'password': 'mypass',
        'roles': []
    },
    {  # Min data
        'email': 'user.2@gmail.com',
        'username': 'User_2',
        'password': 'mypass',
        'roles': []
    },
    {
        'email': 'user.3@gmail.com',
        'username': 'User_3',
        'password': 'mypass',
        'roles': []
    },
    {
        'email': 'user.4@gmail.com',
        'username': 'User_4',
        'password': 'mypass',
        'roles': []
    },
    {
        'email': 'user.5@gmail.com',
        'username': 'User_5',
        'password': 'mypass',
        'roles': []
    }
]

user_valid_data_response = [
    {
        'id': 1,
        'email': 'user.1@gmail.com',
        'username': 'User_1',
        'about': 'About user 1',
        'rating': 1,
        'is_active': False,
        'is_superuser': True,
        'is_email_confirmed': False,
        'roles': []
    },
    {
        'id': 2,
        'email': 'user.2@gmail.com',
        'username': 'User_2',
        'about': '',
        'rating': 0,
        'is_active': True,
        'is_superuser': False,
        'is_email_confirmed': False,
        'roles': []
    },
    {
        'id': 3,
        'email': 'user.3@gmail.com',
        'username': 'User_3',
        'about': '',
        'rating': 0,
        'is_active': True,
        'is_superuser': False,
        'is_email_confirmed': False,
        'roles': []
    },
    {
        'id': 4,
        'email': 'user.4@gmail.com',
        'username': 'User_4',
        'about': '',
        'rating': 0,
        'is_active': True,
        'is_superuser': False,
        'is_email_confirmed': False,
        'roles': []
    },
    {
        'id': 5,
        'email': 'user.5@gmail.com',
        'username': 'User_5',
        'about': '',
        'rating': 0,
        'is_active': True,
        'is_superuser': False,
        'is_email_confirmed': False,
        'roles': []
    },
]

user_nested_response = [
    {
        'id': 1,
        'email': 'user.1@gmail.com',
        'username': 'User_1',
        'about': 'About user 1',
        'rating': 1,
        'is_active': False,
        'is_superuser': True,
        'is_email_confirmed': False,
        'roles': []
    },
    {
        'id': 2,
        'email': 'user.2@gmail.com',
        'username': 'User_2',
        'about': '',
        'rating': 0,
        'is_active': True,
        'is_superuser': False,
        'is_email_confirmed': False,
        'roles': []
    },
    {
        'id': 3,
        'email': 'user.3@gmail.com',
        'username': 'User_3',
        'about': '',
        'rating': 0,
        'is_active': True,
        'is_superuser': False,
        'is_email_confirmed': False,
        'roles': []
    },
    {
        'id': 4,
        'email': 'user.4@gmail.com',
        'username': 'User_4',
        'about': '',
        'rating': 0,
        'is_active': True,
        'is_superuser': False,
        'is_email_confirmed': False,
        'roles': []
    }
]

create_user_invalid_email_data = [
    {
        'email': '@gmail.com',  # invalid
        'username': 'User_3',
        'password': 'mypass',
        'roles': []
    },
    {
        'email': 'user.3@',  # invalid
        'username': 'User_3',
        'password': 'mypass',
        'roles': []
    },
    {
        'email': 'user.3gmail.com',  # invalid
        'username': 'User_3',
        'password': 'mypass',
        'roles': []
    },
]

create_user_invalid_unique_email_data = {
    'email': 'user.1@gmail.com',  # Alredy exist
    'username': 'User_999',
    'password': 'mypass',
    'roles': []
}

user_invalid_email_response = {
    'detail': [
        {
            'loc': ['body', 'email'],
            'msg': 'Email is not valid',
            'type': 'value_error'
        }
    ]
}

create_user_invalid_username_data = [
    {
        'email': 'user.3@gmail.com',
        'username': 'Use',  # Min 4 charters
        'password': 'mypass',
        'roles': []
    },
    {
        'email': 'user.3@gmail.com',
        'username': '_User_3',  # No _,- or . at the beginning
        'password': 'mypass',
        'roles': []
    },
    {
        'email': 'user.3@gmail.com',
        'username': 'User_3_',  # No _,- or . at the end
        'password': 'mypass',
        'roles': []
    },
]

create_user_invalid_unique_username_data = {
    'email': 'user.999@gmail.com',
    'username': 'User_1',  # Alredy exist
    'password': 'mypass',
    'roles': []
}

user_invalid_username_response = {
    'detail': [
        {
            'loc': ['body', 'username'],
            'msg': 'Username is not valid',
            'type': 'value_error'
        }
    ]
}

create_user_invalid_password_data = [
    {
        'email': 'user.3@gmail.com',
        'username': 'User_3',
        'password': 'pass',  # At least 6 characters
        'roles': []
    },
    {
        'email': 'user.3@gmail.com',
        'username': 'User_3',
        'password': 'пароль',  # Latin characters only
        'roles': []
    },
    {
        'email': 'user.3@gmail.com',
        'username': 'User_3',
        'password': '0123456789',  # At least one letter
        'roles': []
    },
]

user_invalid_password_response = {
    'detail': [
        {
            'loc': ['body', 'password'],
            'msg': 'Password is not valid',
            'type': 'value_error'
        }
    ]
}

update_user_valid_data = {
    'about': 'New about',
    'rating': 11,
    'is_active': False,
    'is_superuser': True,
    'password': 'user1newpass',
    'roles': []
}

update_user_valid_data_response = {
    'id': 5,
    'email': 'user.5@gmail.com',
    'username': 'User_5',
    'about': 'New about',
    'rating': 11,
    'is_active': False,
    'is_superuser': True,
    'is_email_confirmed': False,
    'roles': []
}

user_invalid_id_response = {
    'detail': 'User does not exist'
}
