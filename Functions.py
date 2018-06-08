import json
import xmltodict

# Taken from stack overflow, code written by Honest Abe.
# Centers tkinter window.
def center(win):
    win.update_idletasks()
    width = win.winfo_width()
    height = win.winfo_height()
    x = (win.winfo_screenwidth() // 2) - (width // 2)
    y = (win.winfo_screenheight() // 2) - (height // 2)
    win.geometry('{}x{}+{}+{}'.format(width, height, x, y))

# Reads and parses an XML file to JSON.
# NOT WORKING
def xmlParserJSON(filePath):
    with open(filePath, 'r') as f:
        xmlString = f.read()

    #print("XML input (sample.xml):")
    #print(xmlString)

    jsonString = json.dumps(xmltodict.parse(xmlString), indent=4)

    #print("\nJSON output(output.json):")
    #print(jsonString)

    fileName = ((filePath.split("\\")[-1]).split("."))[0]

    with open(fileName + ".json", 'w') as f:
        f.write(jsonString)
