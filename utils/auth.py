import os, datetime
from jose import jwt

SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret")
ALGORITHM = "HS256"

def encode_token(user_id, role=None):
    payload = {
        "sub": user_id,
        "role": role,
        "iat": datetime.datetime.utcnow(),
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=8)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def decode_token(token):
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
