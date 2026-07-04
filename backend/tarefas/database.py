from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")

db = client["database"]

users = db["users"]
projects = db["projects"]
tasks = db["tasks"]
comments = db["comments"]