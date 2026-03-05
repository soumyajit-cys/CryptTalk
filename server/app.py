from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from models import *
from auth import AuthManager
from key_store import KeyStore
from connection_manager import ConnectionManager
import json

app = FastAPI()

auth_manager = AuthManager()
key_store = KeyStore()
manager = ConnectionManager()

# ---------------------------
# Registration
# ---------------------------

@app.post("/register")
def register(req: RegisterRequest):
    auth_manager.register(req.username, req.password)
    key_store.store_key(req.username, req.public_key)
    return {"status": "registered"}

# ---------------------------
# Login
# ---------------------------

@app.post("/login")
def login(req: LoginRequest):
    token = auth_manager.login(req.username, req.password)
    return {"token": token}

# ---------------------------
# Public Key Retrieval
# ---------------------------

@app.get("/public_key/{username}")
def get_public_key(username: str):
    key = key_store.get_key(username)
    return {"public_key": key}


# ===========================
# 🔥 WebSocket Endpoint
# ===========================

@app.websocket("/ws/{token}")
async def websocket_endpoint(websocket: WebSocket, token: str):

    username = auth_manager.validate_token(token)
    if not username:
        await websocket.close()
        return

    await manager.connect(username, websocket)

    try:
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)

            # message format:
            # {
            #   "to_user": "bob",
            #   "nonce": "...",
            #   "ciphertext": "...",
            #   "dh_pub": "..."
            # }

            recipient = message["to_user"]

            # Relay encrypted payload ONLY
            await manager.send_to_user(recipient, {
                "from_user": username,
                "nonce": message["nonce"],
                "ciphertext": message["ciphertext"],
                "dh_pub": message.get("dh_pub")
            })

    except WebSocketDisconnect:
        manager.disconnect(username)