from tkinter import *
import Functions as Funs

win = Tk()
win.title("Bases de Datos 2 - Proyecto 3")
win.geometry("500x185")
Funs.center(win)

# Window frames
frame = Frame(win)
xmlFrame = Frame(win)
collectionFrame = Frame(win)
bottomFrame = Frame(win)
frame.pack()
xmlFrame.pack(side = "top")
collectionFrame.pack(side = "top")
bottomFrame.pack(side = "top")

xmlPathVar = StringVar()

Label(frame, text = "Proyecto 3 - MongoDB", font = "Helvetica 15 bold").pack(side = "top", pady = 10) # Title
Label(xmlFrame, text = "Dirección de archivo XML: ", font = "Helvetica 12").pack(side = "left", padx = 10, pady = 5)
Label(collectionFrame, text = "Nombre de colección: ", font = "Helvetica 12").pack(side = "left", padx = 25, pady = 10)
xmlPath = Entry(xmlFrame, font = "Helvetica 12", textvariable = xmlPathVar)
xmlPath.pack(side = "right", padx = 5, pady = 5)
collectionName = Entry(collectionFrame, font = "Helvetica 12")
collectionName.pack(side = "right", padx = 5, pady = 10)

xmlPathVar.set("C:\\Users\\Daniel\\Documents\\GitKraken\\XMLtoMongo\\reut2-000-simple.xml")

Button(bottomFrame, text = "Cargar", font = "Helvetica 12", command = lambda: Funs.parseXMLtoJSON(xmlPath.get())).pack(side = "bottom", padx = 10, pady = 10)

win.mainloop()
