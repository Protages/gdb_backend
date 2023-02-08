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


class IncorrectImageExtension(Exception):
    def __init__(self, allowed_extensions: list = ['.png', '.jpg', '.jpeg']) -> None:
        self.allowed_extensions = allowed_extensions
        self.status_code = status.HTTP_400_BAD_REQUEST
        extensions_str = ' or '.join(allowed_extensions)
        self.content = {
            'detail': f'Image must be with the {extensions_str} extension'
        }
