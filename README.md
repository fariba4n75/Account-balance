# Bank API with FastAPI

# 📖 Description

This project is a simple Banking API built with FastAPI, SQLAlchemy, and Pydantic.
Users can register, create bank accounts, and check their account balances.
Authentication is handled using JWT (JSON Web Token).

# ⚙️ Features
User registration
User login with JWT authentication
Create a new bank account
Retrieve account balance
SQLite database for storage
# 🚀 Installation & Setup
1. Clone the repository:

git clone https://github.com/username/bank-api.git


cd bank-api

 2. Create a virtual environment & install dependencies
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
pip install -r requirements.txt

 3. Run the server
uvicorn main:app --reload

The API will be available at:

http://127.0.0.1:8000

# 📚 API Documentation

FastAPI automatically generates interactive documentation at:

http://127.0.0.1:8000/docs

Main Endpoints (examples):

POST /users/ → Register a new user

POST /login → Authenticate user and get a JWT token

POST /accounts/ → Create a new bank account

POST /balance/ → Retrieve account balance

# 📂 Project Structure
bank-api/
│-- database.py   # Database configuration (SQLite + SQLAlchemy)
│-- models.py     # Database models (User, Account)
│-- schemas.py    # Pydantic schemas for request/response
│-- main.py       # Main API logic (JWT authentication, routes)
│-- README.md     # Project documentation

# 📝 License

This project is for educational purposes and can be freely used or modified.
