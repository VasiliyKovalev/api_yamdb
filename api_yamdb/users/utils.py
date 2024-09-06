import random

from django.core.mail import send_mail


def generate_code():
    return random.randint(100000, 999999)


def send_confirmation_code(confirmation_code, email):
    send_mail(
        subject='Код подтверждения',
        message=f'Ваш код для получения токена: {confirmation_code}',
        from_email='api_yamdb@example.com',
        recipient_list=[f'{email}'],
        fail_silently=True,
    )
