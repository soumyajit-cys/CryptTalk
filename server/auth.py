import hashlib
import secrets

class AuthManager:
    def __init__(self):
        self.users = {}
        self.sessions = {}

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def register(self, username, password):
        if username in self.users:
            raise Exception("User already exists")

        self.users[username] = self.hash_password(password)

    def login(self, username, password):
        hashed = self.hash_password(password)

        if self.users.get(username) != hashed:
            raise Exception("Invalid credentials")

        token = secrets.token_hex(16)
        self.sessions[token] = username
        return token

    def validate_token(self, token):
        return self.sessions.get(token)
    


    