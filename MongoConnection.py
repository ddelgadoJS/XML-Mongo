from pymongo import *
import ast
import json

# Returns connection to desired database.
def connectMongoDB(host = 'localhost', port = 27017):
    return MongoClient(host, port).proyect3db

# Inserts document into collection.
# Returns inserted document id.
def insertDocument(collection, document):
    return collection.insert_one(document).inserted_id

#
def getDocument(collection, documentId):
    return collection.find('{_id: ObjectId(documentId)}')


db = connectMongoDB()

collection = db.testCollection

print(collection.find({}))

for doc in collection.find({}):
    print(doc)

with open("C:\\Users\\Daniel\\Documents\\GitKraken\\XMLtoMongo\\reut2-000_enhanced.json", 'r') as f:
    xmlString = f.read()

    #json_acceptable_string = xmlString.replace("'", "\"")

    #insertDocument(collection, json.loads(xmlString))

    #collection.insert_many(ast.literal_eval(xmlString))

#print (getDocument(collection, "5b1c64c35abdc121c804fb86"))

print (collection.count())

#insertDocument(collection, {"author": "Mike", "text": "My first blog post!", "tags": ["mongodb", "python", "pymongo"]})

print (collection.count())

#post = {"author": "Mike",
#        "text": "My first blog post!",
#        "tags": ["mongodb", "python", "pymongo"]}

#post_id = db.testCollection.insert_one(post).inserted_id

print (db)

#print (post_id)
