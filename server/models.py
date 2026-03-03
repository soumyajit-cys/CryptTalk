from pydantic import BaseModel
from typing import Optional

class RegisterRequest(BaseModel):
    username: str
    password: str
    public_key: str


class LoginRequest(BaseModel):
    username: str
    password: str


class MessageRequest(BaseModel):
    from_user: str
    to_user: str
    nonce: str
    ciphertext: str
    dh_pub: Optional[str] = None


class MessageResponse(BaseModel):
    from_user: str
    nonce: str
    ciphertext: str
    dh_pub: Optional[str] = None