from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

users = {}
messages = []

class RegisterRequest(BaseModel):
    username: str
    public_key: str

class MessageRequest(BaseModel):
    from_user: str
    to: str
    nonce: str
    ciphertext: str

@app.post("/register")
def register(req: RegisterRequest):
    users[req.username] = req.public_key
    return {"status": "registered"}

@app.get("/public_key/{username}")
def get_public_key(username: str):
    return {"public_key": users.get(username)}

@app.post("/send")
def send_message(msg: MessageRequest):
    messages.append(msg.dict())
    return {"status": "sent"}

@app.get("/messages/{username}")
def get_messages(username: str):
    user_msgs = [m for m in messages if m["to"] == username]
    return user_msgs