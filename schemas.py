from pydantic import BaseModel, Field


# Create Contact Schema (Pydantic Model)
class ContactCreateSchema(BaseModel):
    first_name: str = Field(..., regex="^[a-zA-Z]+$", error_messages={"regex": "Invalid format. Only letters are allowed."})
    last_name: str = Field(..., regex="^[a-zA-Z]+$", error_messages={"regex": "Invalid format. Only letters are allowed."})
    phone_number: str = Field(..., regex="^[0-9]+$", error_messages={"regex": "Invalid format. Only digits are allowed."})
    email: str = Field(..., regex=r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", error_messages={
            "regex": "Invalid email format. Please provide a valid email address."
        })


# Complete Phonebook Schema (Pydantic Model)
class PhonebookSchema(BaseModel):
    id: int
    first_name: str
    last_name: str
    phone_number: str
    email: str

    class Config:
        orm_mode = True
