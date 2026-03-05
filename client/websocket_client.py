import asyncio
import websockets
import json
import requests

SERVER_HTTP = "http://localhost:8000"
SERVER_WS = "ws://localhost:8000/ws"

class SecureWebSocketClient:

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.token = None
        self.websocket = None

    def login(self):
        response = requests.post(
            f"{SERVER_HTTP}/login",
            json={"username": self.username, "password": self.password}
        )
        self.token = response.json()["token"]

    async def connect(self):
        self.websocket = await websockets.connect(
            f"{SERVER_WS}/{self.token}"
        )
        print("Connected to WebSocket server")

    async def send_encrypted(self, encrypted_payload):
        await self.websocket.send(json.dumps(encrypted_payload))

    async def listen(self):
        while True:
            message = await self.websocket.recv()
            data = json.loads(message)
            print(f"Encrypted message received from {data['from_user']}")
            # Decrypt using Double Ratchet here

    async def run(self):
        await self.connect()
        await self.listen()