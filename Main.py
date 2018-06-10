from tkinter import *
import Functions as Funcs
import MongoConnection as Conn

win = Tk()
win.title("Bases de Datos 2 - Proyecto 3")
win.geometry("800x185")
Funcs.center(win)

# Window frames
frame = Frame(win)
xmlFrame = Frame(win)
collectionFrame = Frame(win)
bottomFrame = Frame(win)
frame.pack()
xmlFrame.pack(side = "top")
collectionFrame.pack(side = "top")
bottomFrame.pack(side = "top")

# Test purposes
directoryPathVar = StringVar()

Label(frame, text = "Proyecto 3 - MongoDB", font = "Helvetica 15 bold").pack(side = "top", pady = 10) # Title
Label(xmlFrame, text = "Dirección de archivo XML: ", font = "Helvetica 12").pack(side = "left", padx = 10, pady = 5)
Label(collectionFrame, text = "Nombre de colección: ", font = "Helvetica 12").pack(side = "left", padx = 26, pady = 10)
directoryPath = Entry(xmlFrame, font = "Helvetica 12", textvariable = directoryPathVar, width = 60)
collectionName = Entry(collectionFrame, font = "Helvetica 12", width = 60)
directoryPath.pack(side = "right", padx = 5, pady = 5)
collectionName.pack(side = "right", padx = 5, pady = 10)

# Default text for test purposes.
#directoryPathVar.set("C:\\Users\\Daniel\\Documents\\GitKraken\\XMLtoMongo\\reuters21578")

Button(bottomFrame, text = "Cargar", font = "Helvetica 12", command = lambda: Conn.processPetition(directoryPath.get(), collectionName.get())).pack(side = "bottom", padx = 10, pady = 10)

win.mainloop()
