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
    print("connected to the mongodb database")

    

# @app.on_event("shutdown")
# async def shutdown_db_client():
#     app.mongodb_client.close()

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


# -- Profile Endpoints -- 
@app.get("/api/v1/get/profile")
async def get_profile(current_user: User = Depends(auth.require_user)):
    #
    return {current_user.user_id: {"name": current_user.first_name + current_user.last_name , "email": current_user.email, "language": str}}

# updates profile POST (sends to db to update)
@app.post("/api/v1/update/profile")
async def get_profile(updates: object, current_user: User = Depends(auth.require_user)):
    
    return {current_user: {"name": current_user.first_name + current_user.last_name , "email": current_user.email, "language": str}}
