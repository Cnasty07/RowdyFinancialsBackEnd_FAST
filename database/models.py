import os
import uuid
from typing import Optional, List
from pydantic import BaseModel, Field
from pymongo import MongoClient
import datetime
#main code 
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
    pass

if __name__ == '__main__':
    main() 
