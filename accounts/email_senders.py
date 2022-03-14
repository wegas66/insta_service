from django.conf import settings
from django.core.mail import send_mail


def confirm_email(email, token):
    subject = 'Подтверждение почты'
    body = f'Подтвердите почту на сайте {settings.EMAIL_VERIFY_HOST_BASIC}/{email}/{token}'
    try:
        send = send_mail(
            subject,
            body,
            settings.EMAIL_HOST_USER,
            [email]
        )
        return send
    except Exception as e:
        return False
