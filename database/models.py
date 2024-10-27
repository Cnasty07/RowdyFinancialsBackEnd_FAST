import os
import uuid
from typing import Optional, List
from pydantic import BaseModel, Field
from pymongo import MongoClient
import datetime

#main code 
class MongoDB:
    def __init__(self, uri: str, db_name: str):
        self.client = MongoClient(uri)
        self.db = self.client[db_name]

    def get_collection(self, name: str):
        return self.db[name]
    def create_collection(self, name: str):
        if name not in self.db.list_collection_names():
            self.db.create_collection(name)
        return self.db[name]



class ProfileUser(BaseModel):
    id: str = Field(default_factory=uuid.uuid4,alias="_id")
    last_name: str = Field()
    first_name: str = Field()
    email: str = Field()
    language: dict = Field()
    

class Account(BaseModel):
    id: int
    name: str
    balance: float

class AccountsScreenModel(BaseModel):
    accounts: List[Account]
    deposit_percentage: Optional[float] = 0
    transfer_amount: Optional[float] = None


class Transaction(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    account_id: int
    amount: float
    transaction_type: str  # e.g., 'deposit', 'withdrawal', 'transfer'
    timestamp: str = Field(default_factory=lambda: datetime.datetime.utcnow().isoformat())

class Ledger(BaseModel):
    transactions: List[Transaction] = []

    def add_transaction(self, transaction: Transaction):
        self.transactions.append(transaction)

    def get_transactions(self, account_id: int) -> List[Transaction]:
        return [t for t in self.transactions if t.account_id == account_id]
def main():
    # # MongoDB connection setup
    # client = MongoClient(os.getenv("uri"))
    # db = client[os.getenv("DB_NAME")]
    # profiles_collection = db['profiles']

    # # Create a mock user
    # mock_user = ProfileUser(
    #     last_name="Doe",
    #     first_name="John",
    #     email="john.doe@example.com",
    #     language={"primary": "English", "secondary": "Spanish"}
    # )

    # # Insert the mock user into the MongoDB collection
    # profiles_collection.insert_one(mock_user.dict(by_alias=True))

    # print("Mock user inserted into MongoDB")
    # Initialize MongoDB connection
    db = MongoDB(os.getenv("uri"), os.getenv("DB_NAME"))
    
    # Collections for each model
    profiles_collection = db.create_collection('profiles')
    accounts_collection = db.create_collection('accounts')
    transactions_collection = db.create_collection('transactions')
    ledgers_collection = db.create_collection('ledgers')

if __name__ == '__main__':
    main() 
