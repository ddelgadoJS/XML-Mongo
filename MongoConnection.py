import Parser as Parser
import json
from pymongo import *
from os import listdir
from os.path import isfile, join

# Returns connection to desired database.
def connectMongoDB(databaseName = 'Proyecto3', host = 'localhost', port = 27017):
    return MongoClient(host, port)[databaseName]

# Inserts document into collection.
# Returns inserted document id.
# Example: insertDocument(database, 'testCollection', json.loads(jsonString))
def insertDocument(database, collectionName, document):
    return database[collectionName].insert_one(document).inserted_id

#
def getDocument(collection, documentId):
    return collection.find('{_id: ObjectId(documentId)}')

# Process petition from Main.py
# Receives directory path containing XML files.
def processPetition(directoryPath, collectionName):
    db = connectMongoDB()

    # Generates list of XML files.
    xmlFiles = [f for f in listdir(directoryPath) if isfile(join(directoryPath, f))]

    # Iterating over original XML files.
    for file in xmlFiles:
        Parser.parseXMLtoJSON(directoryPath, file)

    # Generates list of JSON files.
    jsonFiles = [f for f in listdir(directoryPath + "\\JSONs") if isfile(join(directoryPath + "\\JSONs", f))]

    # Iterating over generated JSON files and inserting in MongoDB
    for file in jsonFiles:
        with open(directoryPath + "\\JSONs\\" + file, 'r') as f:
            jsonString = f.read()

        insertDocument(db, collectionName, json.loads(jsonString))
