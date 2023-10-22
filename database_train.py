from pymongo import MongoClient
#
from bson import ObjectId

from model_login import *
from model_train import *
import motor.motor_asyncio
from dotenv import dotenv_values
import os

config = dotenv_values(".env")
DATABASE_URI = config.get("DATABASE_URI")
if os.getenv("DATABASE_URI"): 
    DATABASE_URI = os.getenv("DATABASE_URI") #ensures that if we have a system environment variable, it uses that instead

client = motor.motor_asyncio.AsyncIOMotorClient(DATABASE_URI)

database = client.todoapp
collection = database.trains
user_collection = database.logins

async def fetch_all_trains():
    trains = []   
    cursor = collection.find({})
    async for doc in cursor:
        train = Train(**doc)
        trains.append(train)
    
    return trains

async def fetch_one_train(id):
    doc = await collection.find_one({"id": id}, {"_id": 0})
    return doc

async def create_train(train):
    doc = train.dict()
    print(doc)
    result = await collection.insert_one(doc)
    return result

async def change_train(train):
    print(train)
    id = train.id
    title = train.title
    desc = train.desc
    checked = train.checked
    await collection.update_one({"id": id}, {"$set": {"title": title, "desc": desc, "checked": checked}})
    result = await fetch_one_train(id)
    return result

async def delete_train(id):
    await collection.delete_one({"id": id})
    return True

