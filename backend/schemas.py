import datetime as _dt
from pydantic import BaseModel

class User(BaseModel):
    _id: any
    id_user: int
    firstName: str
    lastName: str
    role: str
    username: str
    password: str
    phone: int

class Login(BaseModel):
    username: str
    password: str

class Product(BaseModel):
    _id: any
    id_product: int
    name: str
    price: int
    stock: int
    barcode: str

class Bill(BaseModel):
    _id: any
    id_bill: int
    total: int
    quantity: int
    salesperson: str
    date: str
    time: str