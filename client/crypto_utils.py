import os
import json
import base64
import uuid
from datetime import datetime, timezone

from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

# -----------------------------
# Key Generation
# -----------------------------

def generate_ecdh_keypair():
    private_key = ec.generate_private_key(ec.SECP384R1())
    public_key = private_key.public_key()
    return private_key, public_key


def serialize_public_key(public_key):
    return public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )


def load_public_key(pem_data):
    return serialization.load_pem_public_key(pem_data)


# -----------------------------
# ECDH Shared Key Derivation
# -----------------------------

def derive_session_key(private_key, peer_public_key):
    shared_key = private_key.exchange(ec.ECDH(), peer_public_key)

    derived_key = HKDF(
        algorithm=hashes.SHA256(),
        length=32,
        salt=None,
        info=b"securechat-session",
    ).derive(shared_key)

    return derived_key


# -----------------------------
# AES-256-GCM Encryption
# -----------------------------

def encrypt_message(session_key, plaintext):
    aesgcm = AESGCM(session_key)
    nonce = os.urandom(12)

    message_id = str(uuid.uuid4())
    timestamp = datetime.now(timezone.utc).isoformat()

    payload = {
        "id": message_id,
        "timestamp": timestamp,
        "message": plaintext
    }

    payload_bytes = json.dumps(payload).encode()

    ciphertext = aesgcm.encrypt(nonce, payload_bytes, None)

    return {
        "nonce": base64.b64encode(nonce).decode(),
        "ciphertext": base64.b64encode(ciphertext).decode()
    }


def decrypt_message(session_key, nonce_b64, ciphertext_b64):
    aesgcm = AESGCM(session_key)

    nonce = base64.b64decode(nonce_b64)
    ciphertext = base64.b64decode(ciphertext_b64)

    decrypted = aesgcm.decrypt(nonce, ciphertext, None)
    return json.loads(decrypted.decode())