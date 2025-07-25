from jose import jwt,JWTError
from datetime import timedelta,datetime

secret_key="131"
algo="HS256"
access_token_expire_sec=20
refresh_token_expire_day=7


def create_access_token(data:dict,expire_time:timedelta|None=None):
    to_encode=data.copy()
    access_token_expire=datetime.utcnow()+(expire_time or timedelta(seconds=access_token_expire_sec))
    to_encode.update({"exp":access_token_expire})
    encoded_jwt=jwt.encode(to_encode,secret_key,algorithm=algo)
    print("JWT Token:", encoded_jwt)

    return encoded_jwt

def create_refresh_token(data:dict,expire_time:timedelta|None=None):
    to_encode=data.copy()
    refresh_token_expire=datetime.utcnow()+(expire_time or timedelta(days=refresh_token_expire_day))
    to_encode.update({"exp":refresh_token_expire})
    encoded_jwt=jwt.encode(to_encode,secret_key,algorithm=algo)
    print("JWT Token:", encoded_jwt)
    return encoded_jwt


def verify_token(token:str,credentials_exception):
    try:
        payload=jwt.decode(token,secret_key,algorithms=[algo])
        username=payload.get("sub")
        if username is None:
            raise credentials_exception
        print("Username from token:", username)
        return username
    except JWTError:
        raise credentials_exception