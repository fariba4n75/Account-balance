from pydantic import BaseModel

# ---------- User ----------
class UserCreate(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    id: int
    username: str

    class Config:
        from_attributes = True   # جایگزین orm_mode

# ---------- Token ----------
class Token(BaseModel):
    access_token: str
    token_type: str

# ---------- Account ----------
class AccountCreate(BaseModel):
    account_number: str
    balance: float

class BalanceRequest(BaseModel):
    account_number: str

class BalanceResponse(BaseModel):
    account_number: str
    balance: float

    class Config:
        from_attributes = True
