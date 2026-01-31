import os
import datetime
from jose import jwt, JWTError, ExpiredSignatureError

SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret")
ALGORITHM = "HS256"

def encode_token(user_id, role=None):
    payload = {
        "sub": str(user_id),  # ensure subject is a string
        "role": role,
        "iat": datetime.datetime.utcnow(),
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=8)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def decode_token(token):
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except ExpiredSignatureError:
        return {"error": "Token has expired"}
    except JWTError:
        return {"error": "Invalid token"}