from pydantic import BaseModel
from typing import Optional

class AddressSchema(BaseModel):
    address: str
    city: str
    state: str
    postalCode: str
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
    username: str
    age: int
    gender: str
    email: str
    phone: str
    birthDate: str
    weight: float
    height: float
    role: str
    university: str
    address: AddressSchema
    company: CompanySchema
    image: str