'''Platforms data for tests'''


create_platform_valid_data = [
    {
        'title': 'Platform 1'
    },
    {
        'title': 'Platform 2'
    },
    {
        'title': 'Platform 3'
    },
    {
        'title': 'Platform 4'
    },
    {
        'title': 'Platform 5'
    }
]

platform_valid_data_response = [
    {
        'id': 1,
        'title': 'Platform 1'
    },
    {
        'id': 2,
        'title': 'Platform 2'
    },
    {
        'id': 3,
        'title': 'Platform 3'
    },
    {
        'id': 4,
        'title': 'Platform 4'
    },
    {
        'id': 5,
        'title': 'Platform 5'
    }
]

create_platform_invalid_data = {
    'bar': 'baz'  # title required
}

create_platform_invalid_data_response = {
    'detail': [
        {
            'loc': ['body', 'title'], 
            'msg': 'field required', 
            'type': 'value_error.missing'
        }
    ]
}

platform_invalid_id_response = {
    'detail': 'Platform does not exist'
}

update_platform_valid_data = {
    'title': 'Platform 5 update'
}

update_platform_valid_data_response = {
    'id': 5,
    'title': 'Platform 5 update'
}
