from bson.objectid import ObjectId
from pymongo import MongoClient

client = MongoClient('mongodb://203.255.92.141:27017', authSource='admin')
db = client['WOS']
col = db['Author']

for author in col:
  print(author)