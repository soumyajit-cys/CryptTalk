import os
import base64
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

class DoubleRatchet:

    def __init__(self, root_key, dh_pair, peer_public_key):
        self.root_key = root_key
        self.DHs = dh_pair
        self.DHr = peer_public_key

        self.send_chain_key = None
        self.recv_chain_key = None

        self._dh_ratchet()

    # -----------------------------
    # DH Ratchet Step
    # -----------------------------

    def _dh_ratchet(self):
        shared_secret = self.DHs.exchange(ec.ECDH(), self.DHr)

        derived = HKDF(
            algorithm=hashes.SHA256(),
            length=64,
            salt=self.root_key,
            info=b"double-ratchet",
        ).derive(shared_secret)

        self.root_key = derived[:32]
        self.send_chain_key = derived[32:]

    # -----------------------------
    # Symmetric Ratchet
    # -----------------------------

    def _derive_message_key(self, chain_key):
        derived = HKDF(
            algorithm=hashes.SHA256(),
            length=64,
            salt=None,
            info=b"message-key",
        ).derive(chain_key)

        new_chain_key = derived[:32]
        message_key = derived[32:]

        return new_chain_key, message_key

    # -----------------------------
    # Encrypt Message
    # -----------------------------

    def encrypt(self, plaintext):
        self.send_chain_key, message_key = self._derive_message_key(
            self.send_chain_key
        )

        aesgcm = AESGCM(message_key)
        nonce = os.urandom(12)

        ciphertext = aesgcm.encrypt(nonce, plaintext.encode(), None)

        return {
            "nonce": base64.b64encode(nonce).decode(),
            "ciphertext": base64.b64encode(ciphertext).decode(),
            "dh_pub": self.DHs.public_key().public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            ).decode()
        }

    # -----------------------------
    # Decrypt Message
    # -----------------------------

    def decrypt(self, nonce_b64, ciphertext_b64):
        self.recv_chain_key, message_key = self._derive_message_key(
            self.recv_chain_key
        )

        aesgcm = AESGCM(message_key)
        nonce = base64.b64decode(nonce_b64)
        ciphertext = base64.b64decode(ciphertext_b64)

        plaintext = aesgcm.decrypt(nonce, ciphertext, None)
        return plaintext.decode()