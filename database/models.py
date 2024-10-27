import os
import uuid
from typing import Optional
from pydantic import BaseModel, Field

#main code 
class ProfileUser(BaseModel):
    id: str = Field(default_factory=uuid.uuid4,alias="_id")
    last_name: str = Field()
    first_name: str = Field()
    name: str = first_name + last_name
    email: str = Field()
    language: dict = Field()
    
    
    class Config:
        allow_population_by_field = True
        schema_extra = {
            "_id": "",
            "name": "Ruben Reyes",
            
        }
        
class AccountsUser(BaseModel):
    id: str = Field()
    
    
class AccountTransfer(BaseModel):
    id: str = Field()

def main():
    pass

if __name__ == '__main__':
    main() 
