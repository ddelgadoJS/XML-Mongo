from tkinter import *
from tkinter.filedialog import askdirectory
import Functions as Funcs
import MongoConnection as Conn

def askDirectory(directoryPathVar):
    directoryPathVar.set(askdirectory())

win = Tk()
win.title("Bases de Datos 2 - Proyecto 3")
win.geometry("800x340")
Funcs.centerWindow(win)

frame = Frame(win)
xmlFrame = Frame(win)
collectionFrame = Frame(win)
databaseFrame = Frame(win)
hostFrame = Frame(win)
portFrame = Frame(win)
bottomFrame = Frame(win)

frame.pack()
xmlFrame.pack(side = "top")
collectionFrame.pack(side = "top")
databaseFrame.pack(side = "top")
hostFrame.pack(side = "top")
portFrame.pack(side = "top")
bottomFrame.pack(side = "top")

directoryPathVar = StringVar()
collectionNameVar = StringVar()
databaseNameVar = StringVar()
hostVar = StringVar()
portNumberVar = IntVar()

Label(frame, text = "Proyecto 3 - MongoDB", font = "Helvetica 15 bold").pack(side = "top", pady = 10)
Label(xmlFrame, text = "Directorio de archivos XML: ", font = "Helvetica 12").pack(side = "left", padx = 5, pady = 10)
Label(collectionFrame, text = "Nombre de colección: ", font = "Helvetica 12").pack(side = "left", padx = 17, pady = 10)
Label(databaseFrame, text = "Nombre de base de datos: ", font = "Helvetica 12").pack(side = "left", padx = 0, pady = 10)
Label(hostFrame, text = "Host: ", font = "Helvetica 12").pack(side = "left", padx = 8, pady = 10)
Label(portFrame, text = "Puerto: ", font = "Helvetica 12").pack(side = "left", padx = 1, pady = 10)

directoryPath = Entry(xmlFrame, font = "Helvetica 12", textvariable = directoryPathVar, width = 60)
collectionName = Entry(collectionFrame, font = "Helvetica 12", textvariable = collectionNameVar, width = 30)
databaseName = Entry(databaseFrame, font = "Helvetica 12", textvariable = databaseNameVar, width = 30)
host = Entry(hostFrame, font = "Helvetica 12", textvariable = hostVar, width = 15)
portNumber = Entry(portFrame, font = "Helvetica 12", textvariable = portNumberVar, width = 15)

directoryPath.pack(side = "right", padx = 0, pady = 10)
collectionName.pack(side = "left", padx = 0, pady = 10)
databaseName.pack(side = "left", padx = 17, pady = 10)
host.pack(side = "left", padx = 10, pady = 10)
portNumber.pack(side = "left", padx = 17, pady = 10)

collectionNameVar.set("ColeccionPrueba")
databaseNameVar.set("Proyecto3")
hostVar.set("localhost")
portNumberVar.set(27017)

Button(bottomFrame, text = "Cargar", font = "Helvetica 12", command = lambda: Conn.processPetition(win, directoryPath.get(), collectionName.get(), databaseName.get(), host.get(), int(portNumber.get()))).pack(side = "left", padx = 0, pady = 15)
Button(bottomFrame, text = "Buscar directorio", font = "Helvetica 12", command = lambda: askDirectory(directoryPathVar)).pack(side = "left", padx = 25, pady = 15)

win.mainloop()
