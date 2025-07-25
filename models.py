from pydantic import BaseModel,Field

class User(BaseModel):
    username:str=Field(...,min_length=1,max_length=14)
    password:str=Field(...,min_length=1,max_length=14)

class Token(BaseModel):
    access_token:str
    token_type:str
    refresh_token:str