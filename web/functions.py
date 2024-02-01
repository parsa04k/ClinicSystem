import random
import string


def generate_temp_password(length=8):
    """Generate a random password"""
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))

