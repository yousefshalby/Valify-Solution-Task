from django.utils.crypto import get_random_string
from django.core.cache import cache


def create_confirmation_number():
    otp = get_random_string(length=6, allowed_chars='1234567890')
    cache.set('otp', otp, 60*10)  # 10 minutes
    return otp
