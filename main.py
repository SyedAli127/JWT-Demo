from fastapi import FastAPI,Depends,HTTPException,status,Header
from fastapi.security import OAuth2PasswordRequestForm,OAuth2PasswordBearer
from passlib.context import CryptContext
from models import User,Token
from auth import verify_token,create_access_token,create_refresh_token


app=FastAPI()

oauth2scheme=OAuth2PasswordBearer(tokenUrl="/login")
pw_context=CryptContext(schemes=["bcrypt"],deprecated="auto")

fake_db={}

def hash_password(password:str):
    return pw_context.hash(password)

def verify_password(plain_password,hashed_password):
    return pw_context.verify(plain_password,hashed_password)

def get_current_user(token:str=Depends(oauth2scheme)):
    credentials_exception=HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Wrong Crendials",
    )
    username=verify_token(token,credentials_exception)
    return username

@app.post("/register")
def register(user:User):
    if user.username in fake_db:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="USer already exist")
    
    hashed_password=hash_password(user.password)
    fake_db[user.username]=hashed_password

    return {"message":"User Registered"}

@app.post("/login",response_model=Token)
def login(form_data:OAuth2PasswordRequestForm=Depends()):
    stored_password=fake_db.get(form_data.username)
    if not stored_password or not verify_password(form_data.password,stored_password):
        raise HTTPException(400,detail="Username or Password not Corrected")
    access_token=create_access_token(data={"sub":form_data.username})
    refresh_token=create_refresh_token(data={"sub":form_data.username})
    
    return {"access_token": access_token,"refresh_token":refresh_token,"token_type":"bearer"}

@app.get("/protected")
def protected_route(token:str=Depends(oauth2scheme),current_user:str=Depends(get_current_user)):
    return {"message": f"Hello, {current_user}. You have access!",
            "token_used":token}

@app.post("/refresh",response_model=Token)
def refresh_route(refresh_token:str=Header(...)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid refresh token"
    )
    try:
        username = verify_token(refresh_token, credentials_exception)
    except:
        raise credentials_exception
    
    new_access_token = create_access_token(data={"sub": username})

    return {
        "access_token": new_access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }

