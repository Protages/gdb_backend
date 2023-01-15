from fastapi import status


class ObjectDoesNotExistException(Exception):
    def __init__(self, obj_name: str | None = None) -> None:
        self.obj_name = obj_name
        self.status_code = status.HTTP_400_BAD_REQUEST
        if obj_name:
            self.detail = f'{obj_name.capitalize()} does not exist'
        else:
            self.detail = 'Object does not exist'
        self.content = {'detail': self.detail}
