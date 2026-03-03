class MessageStore:
    def __init__(self):
        self.messages = []

    def store_message(self, message):
        self.messages.append(message)

    def get_messages_for_user(self, username):
        user_messages = [
            m for m in self.messages if m["to_user"] == username
        ]
        return user_messages