import os
import uuid
from typing import Optional, List
from pydantic import BaseModel, Field
from pymongo import MongoClient

#main code 
class ProfileUser(BaseModel):
    id: str = Field(default_factory=uuid.uuid4,alias="_id")
    last_name: str = Field()
    first_name: str = Field()
    name: str = first_name + last_name
    email: str = Field()
    language: dict = Field()
    
    
    # class Config:
    #     allow_population_by_field = True
    #     schema_extra = {
    #         "_id": "",
    #         "name": "Ruben Reyes",
            
    #     }
class UserProfile(BaseModel):
    name: str
    email: str
    language: str = Field(default='en', regex='^(en|es)$')  # Only allow 'en' or 'es'

# Example usage
user_profile = UserProfile(name="Mock User", email="mockuser@example.com")
print(user_profile)


class Account(BaseModel):
    id: int
    name: str
    balance: float

class AccountsScreenModel(BaseModel):
    accounts: List[Account]
    deposit_percentage: Optional[float] = 0
    transfer_amount: Optional[float] = None

# class AccountsUser(BaseModel):
#     id: str = Field()
    
    
# class AccountTransfer(BaseModel):
#     id: str = Field()

def main():
    pass

if __name__ == '__main__':
    main() 
