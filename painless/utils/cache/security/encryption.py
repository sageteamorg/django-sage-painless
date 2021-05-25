import ast

from Crypto.Cipher import PKCS1_OAEP
from django.conf import settings


def encrypt_message(message):
    """
    encrypt message based on RSA algorithm
    """
    if not hasattr(settings, 'PUBLIC_KEY'):
        raise AttributeError('PUBLIC_KEY must be defined in settings')

    public_key = settings.PUBLIC_KEY
    encryptor = PKCS1_OAEP.new(public_key)
    if type(message) in [list, tuple, set]:
        encrypted_msg = [encryptor.encrypt(x.encode('UTF-8')) for x in message]
    else:
        encrypted_msg = encryptor.encrypt(message.encode('UTF-8'))
    return encrypted_msg


def decrypt_message(encrypted_msg):
    """
    decrypt message based on RSA algorithm
    """
    if not hasattr(settings, 'PRIVATE_KEY'):
        raise AttributeError('PRIVATE_KEY must be defined in settings')

    private_key = settings.PRIVATE_KEY
    decryptor = PKCS1_OAEP.new(private_key)
    if type(encrypted_msg) in [list, tuple, set]:
        decoded_decrypted_msg = [decryptor.decrypt(ast.literal_eval(str(x.decode('UTF-8')))) for x in encrypted_msg]
    else:
        decoded_decrypted_msg = decryptor.decrypt(ast.literal_eval(str(encrypted_msg.decode('UTF-8'))))
    return decoded_decrypted_msg
