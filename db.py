import sys
import pymongo
from pymongo import MongoClient

connection = MongoClient("ds149344.mlab.com", 49344)
db = connection["lazytrip_dev"]
db.authenticate("test", "firstival1")

activities = db.activities

for activity in activities.find({}, {"name": 1, "idActivity": 1}):
  print(activity)