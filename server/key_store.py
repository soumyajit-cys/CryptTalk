class KeyStore:
    def __init__(self):
        self.public_keys = {}

    def store_key(self, username, public_key):
        self.public_keys[username] = public_key

    def get_key(self, username):
        return self.public_keys.get(username)