from pymongo import MongoClient
from bson import ObjectId

from models.model_login import *
from models.model_train import *
import motor.motor_asyncio
from dotenv import dotenv_values
import os

config = dotenv_values(".env")
DATABASE_URI = config.get("DATABASE_URI")
if os.getenv("DATABASE_URI"): 
    DATABASE_URI = os.getenv("DATABASE_URI") #ensures that if we have a system environment variable, it uses that instead

client = motor.motor_asyncio.AsyncIOMotorClient(DATABASE_URI)

database = client.todoapp

user_collection = database.logins
train_collection = database.trains

# train database handling

async def fetch_all_trains():
    trains = []   
    cursor = train_collection.find({})
    async for doc in cursor:
        train = Train(**doc)
        trains.append(train)
    
    return trains

async def fetch_one_train(id):
    train = await train_collection.find_one({"id": id}, {"_id": 0})
    return train

async def create_train(train):
    doc = dict(train)
    print(doc)
    result = await train_collection.insert_one(doc)
    #if not result: raise HTTPException(400)
    return result

async def change_train(train):
    print(train)
    id = train.id
    title = train.title
    desc = train.desc
    checked = train.checked
    await train_collection.update_one({"id": id}, {"$set": {"title": title, "desc": desc, "checked": checked}})
    result = await fetch_one_train(id)
    return result

async def delete_train(id):
    await train_collection.delete_one({"id": id})
    return True

# user database handling

async def fetch_all_users():
    users = []
    cursor = user_collection.find({})
    async for doc in cursor:
        login = Login(**doc)
        users.append(login)
    return users

async def find_user(id):
    result = await user_collection.find_one({"id": id})
    print(result)
    return result

async def create_user(user):
    print(user)
    result = await user_collection.insert_one(user)
    print(result)
    return result

async def delete_user(id):
    doc = await user_collection.find_one({"id": id}, {"_id": 0})
    print(doc)
    return doc