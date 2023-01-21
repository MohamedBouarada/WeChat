from Crypto.PublicKey import RSA
import base64
from cryptography import x509
from cryptography.hazmat.primitives.asymmetric import padding
from Crypto.Cipher import PKCS1_v1_5

from cryptography.hazmat.backends import default_backend
from Crypto.Random import get_random_bytes

from dotenv.main import load_dotenv
import os

load_dotenv()

CA_CLIENT_CERT_DIR = os.environ["CA_CLIENT_CERT_DIR"]
CA_CLIENT_KEY_DIR = os.environ["CA_CLIENT_KEY_DIR"]


def rsa_encrypt(message, receiver_username):

    cert = x509.load_pem_x509_certificate(
        open(CA_CLIENT_CERT_DIR + receiver_username + "_cert.pem", "rb").read(),
        default_backend(),
    )
    pub_key = cert.public_key()
    message = str.encode(message)
    encrypted_message = pub_key.encrypt(message, padding.PKCS1v15())

    encrypted_message = base64.b64encode(encrypted_message)
    return encrypted_message


def rsa_decrypt(encrypted_message, receiver_username):

    rsa_private_key = RSA.importKey(
        open(CA_CLIENT_KEY_DIR + receiver_username + ".key", "r").read()
    )
    rsa_private_key = PKCS1_v1_5.new(rsa_private_key)
    encrypted_message = base64.b64decode(encrypted_message)
    sentinel = get_random_bytes(16)
    decrypted_message = rsa_private_key.decrypt(encrypted_message, sentinel)
    return decrypted_message
