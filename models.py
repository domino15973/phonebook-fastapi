from sqlalchemy import Column, Integer, String
from database import Base


# Define Phonebook class inheriting from Base
class ContactModel(Base):
    __tablename__ = 'phonebook'
    id = Column(Integer, primary_key=True)
    first_name = Column(String(100))
    last_name = Column(String(100))
    phone_number = Column(String(100))
    email = Column(String(100), unique=True)
