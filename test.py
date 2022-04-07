import pymongo
mongoClient = pymongo.MongoClient("mongodb://localhost:27017/")
mongo_db = mongoClient["ml_app"]

collection = mongo_db["process_status"]

r = collection.find_one({"email":"manpreetignite@gmail.com"})
print(r["status"])
