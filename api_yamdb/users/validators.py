from django.core.exceptions import ValidationError


PROHIBITED_USERNAMES = ('me',)


def validate_username_not_prohibited(value):
    if value in PROHIBITED_USERNAMES:
        raise ValidationError(f'{value} - недопустимое имя пользователя!')
    return value
