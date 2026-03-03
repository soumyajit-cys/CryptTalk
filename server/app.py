from fastapi import FastAPI, HTTPException, Header
from models import *
from auth import AuthManager
from key_store import KeyStore
from message_store import MessageStore

app = FastAPI()

auth_manager = AuthManager()
key_store = KeyStore()
message_store = MessageStore()

# ---------------------------
# User Registration
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
# Get Public Key
# ---------------------------

@app.get("/public_key/{username}")
def get_public_key(username: str):
    key = key_store.get_key(username)
    if not key:
        raise HTTPException(status_code=404, detail="User not found")
    return {"public_key": key}

# ---------------------------
# Send Encrypted Message
# ---------------------------

@app.post("/send")
def send_message(msg: MessageRequest, token: str = Header(...)):
    sender = auth_manager.validate_token(token)

    if not sender or sender != msg.from_user:
        raise HTTPException(status_code=401, detail="Unauthorized")

    message_store.store_message(msg.dict())
    return {"status": "sent"}

# ---------------------------
# Retrieve Messages
# ---------------------------

@app.get("/messages")
def get_messages(token: str = Header(...)):
    username = auth_manager.validate_token(token)
    if not username:
        raise HTTPException(status_code=401, detail="Unauthorized")

    messages = message_store.get_messages_for_user(username)
    return messages