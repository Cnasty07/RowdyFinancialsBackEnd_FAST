from fastapi import FastAPI, Depends
from propelauth_fastapi import init_auth, init_base_auth, User , TokenVerificationMetadata
from pymongo import MongoClient
from contextlib import asynccontextmanager
from dotenv import dotenv_values

config = dotenv_values(".env")

from database.models import ProfileUser
import uvicorn
from fastapi.openapi.utils import get_openapi



# -- MONGODB -- 
@asynccontextmanager
async def lifespan(app: FastAPI):
    app.mongodb_client = MongoClient(config['uri'])
    app.database = app.mongodb_client[config['DB_NAME']]
    print("Connected to the MongoDB database")
    
    yield

    app.mongodb_client.close()
    print("Disconnected from the MongoDB database")

app = FastAPI(lifespan=lifespan)

auth = init_auth(auth_url="https://0586364.propelauthtest.com",api_key= config["backend_api_key"],debug_mode=True)
            

@app.get("/", tags=["root"])
async def root():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Rowdy Financials API",
        version="1.0.0",
        description="API for Rowdy Financials",
        routes=app.routes,
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema


@app.get("/api/v1/home", tags=["home"])
async def home(current_user: User = Depends(auth.require_user)):
    users_collection = app.database["users"]
    user_profile = users_collection.find_one({"user_id": current_user.user_id}, {"_id": 0, "user_id": 1, "first_name": 1, "last_name": 1, "email": 1, "language": 1})
    
    if user_profile:
        return {"status": "success", "profile": user_profile}
    else:
        return {"status": "error", "message": "User profile not found"}

@app.post("/api/v1/login")
async def login(user: User = Depends(auth.require_user)):
    # Generate a new access token for the user
    access_token = auth.generate_access_token(user_id=user.user_id)
    return {"access_token": access_token}


@app.post("/api/v1/add_user", response_model=ProfileUser)
async def add_user(new_user: ProfileUser, current_user: User = Depends(auth.require_user)):
    users_collection = app.database["users"]
    
    # Check if the user already exists
    existing_user = users_collection.find_one({"user_id": new_user.user_id})
    if existing_user:
        return {"status": "error", "message": "User already exists"}
    
    # Add the new user to the database
    user_data = new_user.dict()
    user_data["language"] = "en"  # Default language
    users_collection.insert_one(user_data)
    
    return {"status": "success", "message": "User added successfully"}


# add new user to db after sign up
@app.post("/api/v1/add_user")
async def add_user(new_user: User = Depends(auth.require_user)):
    users_collection = app.database["users"]
    
    # Check if the user already exists
    existing_user = users_collection.find_one({"user_id": new_user.user_id})
    if existing_user:
        return {"status": "error", "message": "User already exists"}
    
    # Add the new user to the database
    user_data = {
        "user_id": new_user.user_id,
        "first_name": new_user.first_name,
        "last_name": new_user.last_name,
        "email": new_user.email,
        "language": "en"  # Default language
    }
    users_collection.insert_one(user_data)
    
    return {"status": "success", "message": "User added successfully"}


# checks who user is (make sure to get user access token)
@app.get("/api/v1/whoami")
async def read_root(current_user: User = Depends(auth.require_user)):
    return {"Hello": f"{current_user.user_id}"}


# -- Refresh PropelAuth token for user
@app.post("/api/v1/token/refresh")
async def refresh_token(current_user: User = Depends(auth.require_user)):
    new_token = auth.generate_access_token(user_id=current_user.user_id)
    return {"access_token": new_token}


# -- Accounts Endpoints -- 


@app.post("/api/v1/update/accounts/transfer")
async def transfer_accounts(from_account_id: str, to_account_id: str, amount: float, current_user: User = Depends(auth.require_user)):
    accounts_collection = app.database["accounts"]
    
    # Find the from and to accounts and ensure they belong to the current user
    from_account = accounts_collection.find_one({"_id": from_account_id, "user_id": current_user.user_id})
    to_account = accounts_collection.find_one({"_id": to_account_id, "user_id": current_user.user_id})
    
    if from_account and to_account:
        # Check if the from_account has enough balance
        if from_account["balance"] >= amount:
            # Perform the transfer
            new_from_balance = from_account["balance"] - amount
            new_to_balance = to_account["balance"] + amount
            
            accounts_collection.update_one({"_id": from_account_id}, {"$set": {"balance": new_from_balance}})
            accounts_collection.update_one({"_id": to_account_id}, {"$set": {"balance": new_to_balance}})
            
            return {"status": "success", "new_from_balance": new_from_balance, "new_to_balance": new_to_balance}
        else:
            return {"status": "error", "message": "Insufficient funds in the from account"}
    else:
        return {"status": "error", "message": "One or both accounts not found or do not belong to the user"}


# -- Profile Endpoints -- 
@app.post("/api/v1/update/profile/language")
async def update_profile_language(language: str, current_user: User = Depends(auth.require_user)):
    users_collection = app.database["users"]
    
    # Update the user's preferred language
    result = users_collection.update_one(
        {"user_id": current_user.user_id},
        {"$set": {"language": language}}
    )
    user_profile = users_collection.find_one({"user_id": current_user.user_id}, {"_id": 0, "user_id": 1, "first_name": 1, "last_name": 1, "email": 1, "language": 1})
    if user_profile:
        return {"status": "success", "profile": user_profile}
    
    if result.modified_count == 1:
        return {"status": "success", "message": "Language updated successfully"}
    else:
        return {"status": "error", "message": "Failed to update language"}


if __name__ == "__main__":
    uvicorn.run(app)
