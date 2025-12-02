import os
import datetime
from jose import jwt

# Secret key and algorithm
SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret")
ALGORITHM = "HS256"

def encode_token(customer_id, role=None):
    """
    Create a JWT token for a specific user/customer.
    - customer_id: the subject of the token
    - role: optional role string (admin, mechanic, customer)
    """
    payload = {
        "sub": customer_id,
        "role": role,
        "iat": datetime.datetime.utcnow(),
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=8)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def decode_token(token):
    """
    Decode a JWT token and return the payload.
    Raises exceptions if invalid or expired.
    """
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
