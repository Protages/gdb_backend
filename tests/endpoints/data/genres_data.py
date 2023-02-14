'''Genres data for tests'''


create_genre_valid_data = [
    {
        'title': 'Genre 1'
    },
    {
        'title': 'Genre 2'
    },
    {
        'title': 'Genre 3'
    },
    {
        'title': 'Genre 4'
    },
    {
        'title': 'Genre 5'
    }
]

genre_valid_data_response = [
    {
        'id': 1,
        'title': 'Genre 1'
    },
    {
        'id': 2,
        'title': 'Genre 2'
    },
    {
        'id': 3,
        'title': 'Genre 3'
    },
    {
        'id': 4,
        'title': 'Genre 4'
    },
    {
        'id': 5,
        'title': 'Genre 5'
    }
]

create_genre_invalid_data = {
    'bar': 'baz'  # title required
}

create_genre_invalid_data_response = {
    'detail': [
        {
            'loc': ['body', 'title'], 
            'msg': 'field required', 
            'type': 'value_error.missing'
        }
    ]
}

genre_invalid_id_response = {
    'detail': 'Genre does not exist'
}

update_genre_valid_data = {
    'title': 'Genre 5 update'
}

update_genre_valid_data_response = {
    'id': 5,
    'title': 'Genre 5 update'
}
