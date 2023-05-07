from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from django.conf import settings

def create_activation_code(user):
    user.actiovation_code = get_random_string(10)
    user.save()


def send_activation_code(user):
    message = f"""
    рахмет досум за регистрацию! ме сага код активации {user.actiovation_code}
    """
    send_mail(
        subject='активация аккаунта',
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[user.email],
        fail_silently=False 
    )