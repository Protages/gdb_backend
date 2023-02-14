'''Roles data for tests'''


create_role_valid_data = [
    {
        'title': 'Role 1'
    },
    {
        'title': 'Role 2'
    },
    {
        'title': 'Role 3'
    },
    {
        'title': 'Role 4'
    },
    {
        'title': 'Role 5'
    }
]

role_valid_data_response = [
    {
        'id': 1,
        'title': 'Role 1'
    },
    {
        'id': 2,
        'title': 'Role 2'
    },
    {
        'id': 3,
        'title': 'Role 3'
    },
    {
        'id': 4,
        'title': 'Role 4'
    },
    {
        'id': 5,
        'title': 'Role 5'
    }
]

create_role_invalid_data = {
    'bar': 'baz'  # title required
}

create_role_invalid_data_response = {
    'detail': [
        {
            'loc': ['body', 'title'], 
            'msg': 'field required', 
            'type': 'value_error.missing'
        }
    ]
}

role_invalid_id_response = {
    'detail': 'Role does not exist'
}

update_role_valid_data = {
    'title': 'Role 1 update'
}

update_role_valid_data_response = {
    'id': 1,
    'title': 'Role 1 update'
}
