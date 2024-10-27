import os
from fastapi import FastAPI
from pymongo import MongoClient

app = FastAPI()

#main code 
@app.on_event("startup")
def startup_db_client():
    app.mongodb_client = MongoClient(config)
    

@app.on_event("shutdown")
def shutdown_db_client():
    app.mongo_client.close()
    
def main():
    pass

if __name__ == '__main__':
    main() 
