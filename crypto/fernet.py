from django.conf import settings
from cryptography.fernet import Fernet


def encrypt_data(data: str) -> str:
    fernet = Fernet(key=settings.FERNET_KEY)
    encrypted_data = fernet.encrypt(data=data.encode())
    return encrypted_data.decode('utf-8')


def decrypt_data(data: str) -> str:
    fernet = Fernet(key=settings.FERNET_KEY)
    decrypted_data = fernet.decrypt(data.encode()).decode()
    return decrypted_data
