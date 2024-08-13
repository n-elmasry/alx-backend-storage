#!/usr/bin/env python3
from pymongo import MongoClient

client = MongoClient()
db = client.logs
collection = db.nginx

logs = collection.count_documents({})

print(f'{logs} logs')

print('Methods:')

methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]

for method in methods:
    count = collection.count_documents({"method": method})
    print(f"\tmethod {method}: {count}")

status_check = collection.count_documents({"path": "/status"})
print(f"{status_check} status check")
