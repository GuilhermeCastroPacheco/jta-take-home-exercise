from pydantic import BaseModel
from typing import Optional

class AddressSchema(BaseModel):
    city: str
    state: str
    country: str

class CompanySchema(BaseModel):
    name: str
    department: str
    title: str
    address: AddressSchema

class UserSchema(BaseModel):
    id: int
    firstName: str
    lastName: str
    age: int
    gender: str
    email: str
    birthDate: str
    role: str
    university: str
    address: AddressSchema
    company: CompanySchema
    image: str