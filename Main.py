from tkinter import *
from tkinter.filedialog import askdirectory
import Functions as Funcs
import MongoConnection as Conn

def askDirectory(directoryPathVar):
    directoryPathVar.set(askdirectory())

win = Tk()
win.title("Bases de Datos 2 - Proyecto 3")
win.geometry("800x250")
Funcs.center(win)

# Window frames
frame = Frame(win)
xmlFrame = Frame(win)
collectionFrame = Frame(win)
databaseFrame = Frame(win)
bottomFrame = Frame(win)
frame.pack()
xmlFrame.pack(side = "top")
collectionFrame.pack(side = "top")
databaseFrame.pack(side = "top")
bottomFrame.pack(side = "top")

# Test purposes
directoryPathVar = StringVar()
collectionNameVar = StringVar()
databaseNameVar = StringVar()

Label(frame, text = "Proyecto 3 - MongoDB", font = "Helvetica 15 bold").pack(side = "top", pady = 10)
Label(xmlFrame, text = "Directorio de archivos XML: ", font = "Helvetica 12").pack(side = "left", padx = 5, pady = 10)
Label(collectionFrame, text = "Nombre de colección: ", font = "Helvetica 12").pack(side = "left", padx = 17, pady = 10)
Label(databaseFrame, text = "Nombre de base de datos: ", font = "Helvetica 12").pack(side = "left", padx = 0, pady = 10)
directoryPath = Entry(xmlFrame, font = "Helvetica 12", textvariable = directoryPathVar, width = 60)
collectionName = Entry(collectionFrame, font = "Helvetica 12", textvariable = collectionNameVar, width = 30)
databaseName = Entry(databaseFrame, font = "Helvetica 12", textvariable = databaseNameVar, width = 30)
directoryPath.pack(side = "right", padx = 5, pady = 10)
collectionName.pack(side = "left", padx = 5, pady = 10)
databaseName.pack(side = "left", padx = 4, pady = 10)

# Default text for test purposes.
#directoryPathVar.set("C:\\Users\\Daniel\\Documents\\GitKraken\\XMLtoMongo\\reuters21578")
collectionNameVar.set("ColeccionPrueba")
databaseNameVar.set("Proyecto3")

Button(bottomFrame, text = "Cargar", font = "Helvetica 12",
       command = lambda: Conn.processPetition(directoryPath.get(), collectionName.get(), databaseName.get())
      ).pack(side = "left", padx = 0, pady = 15)
Button(bottomFrame, text = "Buscar directorio", font = "Helvetica 12",
       command = lambda: askDirectory(directoryPathVar)).pack(side = "left", padx = 25, pady = 15)

win.mainloop()
