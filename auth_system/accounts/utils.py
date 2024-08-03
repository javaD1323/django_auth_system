import random
import redis
from django.conf import settings
from django.core.exceptions import ValidationError
from .models import User

redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)

OTP_EXPIRY_MINUTES = 5
MAX_FAILED_ATTEMPTS = 3
BLOCK_TIME = 3600


def send_otp(phone_number):
    otp_code = random.randint(1000, 9999)
    redis_client.setex(f"otp:{phone_number}", OTP_EXPIRY_MINUTES * 60, otp_code)
    print(f"OTP for {phone_number}: {otp_code}")
    return otp_code


def verify_otp(phone_number, code):
    stored_code = redis_client.get(f"otp:{phone_number}")
    if stored_code is None or stored_code.decode('utf-8') != code:
        raise ValidationError("Invalid or expired OTP.")
    redis_client.delete(f"otp:{phone_number}")
    return True


def authenticate_user(phone_number, password):
    try:
        user = User.objects.get(phone_number=phone_number)
        if user.check_password(password):
            return user
    except User.DoesNotExist:
        return None
    return None


def record_failed_attempt(ip_address):
    key = f"failed_attempts:{ip_address}"
    attempts = redis_client.get(key)

    if attempts is None:
        redis_client.setex(key, BLOCK_TIME, 1)
    else:
        attempts = int(attempts) + 1
        redis_client.set(key, attempts)
        if attempts >= MAX_FAILED_ATTEMPTS:
            block_ip(ip_address)

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def block_ip(ip_address):
    redis_client.setex(f"blocked:{ip_address}", BLOCK_TIME, 1)


def is_blocked(ip_address):
    return redis_client.exists(f"blocked:{ip_address}")
