import os
from crypto_utils import generate_ecdh_keypair, serialize_public_key

KEY_FILE = "client_private.pem"

def initialize_keys():
    private_key, public_key = generate_ecdh_keypair()

    with open(KEY_FILE, "wb") as f:
        f.write(private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        ))

    return private_key, public_key