from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta

import models, schemas
from database import engine, Base, get_db

# ---------- DB ----------
Base.metadata.create_all(bind=engine)

# ---------- Security ----------
SECRET_KEY = "e5s^#+zsm&06)n-_rjo*9lr%(etlcj@j8$!%=3-er(^j5f@5d_"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI()

# ---------- Helpers ----------
def get_password_hash(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = db.query(models.User).filter(models.User.username == username).first()
    if user is None:
        raise credentials_exception
    return user

# ---------- Routes ----------
@app.post("/register", response_model=schemas.UserResponse)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    hashed_pw = get_password_hash(user.password)
    new_user = models.User(username=user.username, hashed_password=hashed_pw)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.post("/token", response_model=schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/create-account")
def create_account(account: schemas.AccountCreate, 
                   db: Session = Depends(get_db), 
                   current_user: models.User = Depends(get_current_user)):
    # چک کردن تکراری بودن شماره حساب
    existing = db.query(models.Account).filter(models.Account.account_number == account.account_number).first()
    if existing:
        raise HTTPException(status_code=400, detail="Account number already exists")

    new_account = models.Account(
        account_number=account.account_number,
        balance=account.balance,
        owner_id=current_user.id
    )
    db.add(new_account)
    db.commit()
    db.refresh(new_account)
    return {"msg": "Account created", "account_number": new_account.account_number}





@app.post("/balance", response_model=schemas.BalanceResponse)
def get_balance(request: schemas.BalanceRequest, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    account = db.query(models.Account).filter(
        models.Account.account_number == request.account_number,
        models.Account.owner_id == current_user.id
    ).first()
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    return account
