import asyncio
from typing import List
from fastapi import FastAPI, HTTPException
from pymongo import MongoClient
from bson.json_util import dumps, loads
from bson.objectid import ObjectId
import jwt
from fastapi.encoders import jsonable_encoder
import database
import schemas
import logging

logging.basicConfig(level=logging.DEBUG)

app = FastAPI()

client = database.mongoDB

db = client["jaiheng101"]
collectionUser = db["user"]
collectionProducts = db["products"]
collectionBills = db["bills"]
collectionLogs = db["logs"]

dbLogin = client["logins"]
collectionLogin = dbLogin["login"]

SECRET_KEY = "cairocoders123456789"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 800

login = schemas.Login
User = schemas.User
Product = schemas.Product
Bill = schemas.Bill


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/register_user")
async def register(login_item: User):
    data = jsonable_encoder(login_item)
    login = collectionLogin.insert_one(login_item.dict())

    if login is None:
        raise HTTPException(status_code=404, detail="register failed")

    if login:
        return {"register": login}
    else:
        raise HTTPException(status_code=401, detail={"register": "failed"})


@app.post("/login_user")
async def login_user(login_item: login):
    data = jsonable_encoder(login_item)
    login = collectionLogin.find_one(login_item.dict())

    if login is None:
        raise HTTPException(status_code=404, detail="Login failed")

    username_db = login["username"]
    password_db = login["password"]

    if username_db == data["username"] and password_db == data["password"]:
        encoded_jwt = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
        return {"Login": "success", "token": encoded_jwt}
    else:
        raise HTTPException(status_code=401, detail={"Login": "failed"})


# Product Endpoints
# Get all product
@app.get("/products", response_model=List[Product])
async def get_all_products():
    products = list(collectionProducts.find({}))
    return products


# Get a product by id
@app.get("/products/{product_id}", response_model=Product)
async def get_product(product_id: str):
    product = collectionProducts.find_one({"_id": ObjectId(product_id)})
    if product:
        return product
    else:
        raise HTTPException(status_code=404, detail="Product not found")


# Add new product
@app.post("/products", response_model=Product)
async def add_product(product: Product):
    inserted_product = collectionProducts.insert_one(product.dict())
    return product


# Edit a product
@app.put("/products/{product_id}", response_model=Product)
async def edit_product(product_id: int, product_data: Product):
    updated_product = collectionProducts.update_one(
        {"id_product": product_id},
        {"$set": product_data.dict()},
    )
    if updated_product.modified_count == 1:
        return product_data
    else:
        raise HTTPException(status_code=404, detail="Product not found")


# Delete a product by id
@app.delete("/products/{product_id}")
async def delete_product(product_id: int):
    deleted_product = collectionProducts.delete_one({"id_product": product_id})
    if deleted_product.deleted_count == 1:
        return {"message": "Product deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Product not found")


# User Endpoints
# Get all user
@app.get("/users", response_model=List[User])
async def get_all_users():
    users = list(collectionUser.find({}))
    return users


# Add new user
@app.post("/users", response_model=User)
async def add_users(user: User):
    inserted_user = collectionUser.insert_one(user.dict())
    return user


# Edit user
@app.put("/users/{user_id}", response_model=User)
async def edit_user(user_id: int, user_data: User):
    updated_user = collectionUser.update_one(
        {"id_user": user_id},
        {"$set": user_data.dict()},
    )
    if updated_user.modified_count == 1:
        return user_data
    else:
        raise HTTPException(status_code=404, detail="Users not found")


# Delete user
@app.delete("/users/{user_id}")
async def delete_user(user_id: int):
    deleted_user = collectionUser.delete_one({"id_user": user_id})
    if deleted_user.deleted_count == 1:
        return {"message": "Users deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Users not found")


# Bill Endpoints
# Get all bills
@app.get("/bills", response_model=List[Bill])
async def get_all_bills():
    bills = list(collectionBills.find({}))
    return bills


# Add new bill
@app.post("/bills", response_model=Bill)
async def add_bills(bill: Bill):
    inserted_bill = collectionBills.insert_one(bill.dict())
    return bill


# Edit bill
@app.put("/bills/{bill_id}", response_model=Bill)
async def edit_bill(bill_id: int, bill_data: Bill):
    updated_bill = collectionBills.update_one(
        {"id_bill": bill_id},
        {"$set": bill_data.dict()},
    )
    if updated_bill.modified_count == 1:
        return bill_data
    else:
        raise HTTPException(status_code=404, detail="Bills not found")


# Delete bill
@app.delete("/bills/{bill_id}")
async def delete_bill(bill_id: int):
    deleted_bill = collectionBills.delete_one({"id_bill": bill_id})
    if deleted_bill.deleted_count == 1:
        return {"message": "Bills deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Bills not found")
