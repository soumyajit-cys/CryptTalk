import requests
import base64
from crypto_utils import *
from replay_protection import ReplayProtector

SERVER_URL = "http://localhost:8000"

class SecureClient:

    def __init__(self, username):
        self.username = username
        self.private_key, self.public_key = generate_ecdh_keypair()
        self.replay_protector = ReplayProtector()
        self.session_keys = {}

    def register(self):
        requests.post(f"{SERVER_URL}/register", json={
            "username": self.username,
            "public_key": serialize_public_key(self.public_key).decode()
        })

    def get_peer_key(self, peer):
        response = requests.get(f"{SERVER_URL}/public_key/{peer}")
        return load_public_key(response.json()["public_key"].encode())

    def establish_session(self, peer):
        peer_key = self.get_peer_key(peer)
        session_key = derive_session_key(self.private_key, peer_key)
        self.session_keys[peer] = session_key

    def send_message(self, peer, message):
        session_key = self.session_keys[peer]
        encrypted = encrypt_message(session_key, message)

        requests.post(f"{SERVER_URL}/send", json={
            "from": self.username,
            "to": peer,
            "nonce": encrypted["nonce"],
            "ciphertext": encrypted["ciphertext"]
        })

    def receive_messages(self):
        response = requests.get(f"{SERVER_URL}/messages/{self.username}")
        messages = response.json()

        for msg in messages:
            session_key = self.session_keys[msg["from"]]
            payload = decrypt_message(
                session_key,
                msg["nonce"],
                msg["ciphertext"]
            )

            self.replay_protector.validate(payload, msg["nonce"])
            print(f"[{msg['from']}]: {payload['message']}")