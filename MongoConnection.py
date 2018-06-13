import Parser as Parser
import json
from pymongo import *
from os import listdir
from os.path import isfile, join
from tkinter import messagebox

# Returns connection to desired database.
def connectMongoDB(databaseName = 'Proyecto3', host = 'localhost', port = 27017):
    return MongoClient(host, port)[databaseName]

# Example: insertDocument(database, 'testCollection', json.loads(jsonString))
def insertDocument(database, collectionName, document):
    database[collectionName].insert_one(document).inserted_id

# Process petition from Main.py
# Receives directory path containing XML files.
def processPetition(win, directoryPath, collectionName, databaseName, host, port):
    db = connectMongoDB(databaseName = databaseName, host = host, port = port)

    # Generates list of XML files.
    xmlFiles = [f for f in listdir(directoryPath) if isfile(join(directoryPath, f))]

    messagebox.showinfo("Process", "Por favor, presione el botón 'OK' y espere unos segundos.")

    # Iterating over original XML files.
    fileCount = 0
    for file in xmlFiles:
        Parser.enhanceXML(db, collectionName, directoryPath, file)

    messagebox.showinfo("Process", "Se han cargado los archivos exitosamente.")
