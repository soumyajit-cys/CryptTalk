from fastapi import Header, HTTPException

def get_current_user(token: str, auth_manager):
    username = auth_manager.validate_token(token)
    if not username:
        raise HTTPException(status_code=401, detail="Invalid token")
    return username