from datetime import datetime, timezone
import time

class ReplayProtector:
    def __init__(self):
        self.seen_ids = set()
        self.seen_nonces = set()
        self.max_skew_seconds = 60

    def validate(self, payload, nonce):
        message_id = payload["id"]
        timestamp = datetime.fromisoformat(payload["timestamp"])

        # Check replayed ID
        if message_id in self.seen_ids:
            raise Exception("Replay detected: duplicate message ID")

        # Check nonce reuse
        if nonce in self.seen_nonces:
            raise Exception("Replay detected: duplicate nonce")

        # Timestamp freshness check
        now = datetime.now(timezone.utc)
        delta = abs((now - timestamp).total_seconds())

        if delta > self.max_skew_seconds:
            raise Exception("Stale message detected")

        self.seen_ids.add(message_id)
        self.seen_nonces.add(nonce)

        return True