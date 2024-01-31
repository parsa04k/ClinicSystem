from django.contrib.auth.models import User
from django.core.mail import send_mail
import random
import string
import ctypes

def generate_temp_password(length=8):
    """Generate a random password"""
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))

