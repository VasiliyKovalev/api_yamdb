from django.core.exceptions import ValidationError
from django.core.mail import send_mail

from api_yamdb.settings import EMAIL_HOST_USER


def send_confirmation_code(confirmation_code, email):
    send_mail(
        subject='Код подтверждения',
        message=f'Ваш код для получения токена: {confirmation_code}',
        from_email=EMAIL_HOST_USER,
        recipient_list=[email],
        fail_silently=True,
    )


def validate_username_not_me(value):
    if value == 'me':
        raise ValidationError('Недопустимое имя пользователя!')
    return value
