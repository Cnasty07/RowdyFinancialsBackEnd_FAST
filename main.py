from fastapi import FastAPI, Depends
from propelauth_fastapi import init_auth, init_base_auth, User , TokenVerificationMetadata
from pymongo import MongoClient
from dotenv import dotenv_values
import os

config = dotenv_values(".env")

app = FastAPI()

auth = init_auth(auth_url="https://0586364.propelauthtest.com",api_key= config["backend_api_key"],debug_mode=True)

# -- MONGODB -- 

#main code 
@app.on_event("startup")
async def startup_db_client():
    app.mongodb_client = MongoClient(config['uri'])
    app.database = app.mongodb_client[config['DB_NAME']]
    print("Connected to the MongoDB database")

@app.on_event("shutdown")
async def shutdown_db_client():
    app.mongodb_client.close()
    print("Disconnected from the MongoDB database")


# checks who user is (make sure to get user access token)
@app.get("/api/v1/whoami")
async def read_root(current_user: User = Depends(auth.require_user)):
    return {"Hello": f"{current_user.user_id}"}


# -- Accounts Endpoints -- 
# needs to authenticate token and then retrieve users balances
@app.get("/api/v1/get/accounts")
async def get_accounts(current_user: User = Depends(auth.require_user)):
    #
    return {"accounts": {"checkings": int , "savings": int}}

@app.get("api/v1/update/accounts/transfer")
async def transfer_accounts(current_user: User = Depends(auth.require_user)):
    #
    return {}



# 
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
    
    if result.modified_count == 1:
        return {"status": "success", "message": "Language updated successfully"}
    else:
        return {"status": "error", "message": "Failed to update language"}

# @app.get("/api/v1/get/profile")
# async def get_profile(current_user: User = Depends(auth.require_user)):
#     #
#     return {current_user.user_id: {"name": current_user.first_name + current_user.last_name , "email": current_user.email, "language": str}}

# # updates profile POST (sends to db to update)
# @app.post("/api/v1/update/profile")
# async def get_profile(updates: object, current_user: User = Depends(auth.require_user)):
    
#     return {current_user: {"name": current_user.first_name + current_user.last_name , "email": current_user.email, "language": str}}
