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
def parseXMLtoJSON(filePath):
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

def updateXML(filePath, collectionName):
    with open(filePath, 'r') as f:
        xmlString = f.read()

    tagContent = ""
    xmlStringSimple = ""
    tag = ""
    reutersContent = ""
    stack = []
    #for i in range(1, len(xmlString)):
    for i in xmlString:
        # Gets tag
        # If stack[-1] == '<' a tag is being parsed.
        if i == '<' or (len(stack) > 0 and stack[-1] == '<'):
            # Tag's start.
            if len(stack) == 0 or stack[-1] != '<':
                tag = "<"
                stack.append(i) # Adds '<' to know it's parsing a tag.

            # Tag's end.
            elif i == '>':
                stack.pop() # Pops '<'.
                tag += i
                # Checks if it's starting tag or ending tag.
                if tag[1] == '/':
                    if (tag == "</DATE>" or tag == "</TOPICS>" or
                       tag == "</PLACES>" or tag == "</PEOPLE>" or
                       tag == "</ORGS>" or tag == "</EXCHANGES>" or
                       tag == "</TEXT>" or tag == "</TITLE>" or
                       tag == "</AUTHOR>" or tag == "</DATELINE>" or
                       tag == "</BODY>" or tag == "</REUTERS>" or
                       tag == "</COLLECTION>"):

                        # COLLECTION case: change name given by user.
                        if tag == "</COLLECTION>":
                            tag = '</' + collectionName + '>'

                        elif tag == "</TITLE>":
                            tagContent = tagContent[5:]

                        elif tag == "</BODY>":
                            tagContent = tagContent[:-4]

                        xmlStringSimple += tagContent
                        xmlStringSimple += tag

                        if len(stack) > 0 and stack[-1] == tag[0] + tag[2:]: # Looks for ending tag in stack.
                            stack.pop() # Pops opening tag.
                            tagContent = ""

                        else:
                            print ("Error: opening tag not found.")

                    else:
                        tagContent = ""
                        print ("Tag not added: " + tag)

                # First line case.
                elif tag[1] == '?':
                    print ("First line ignored.")

                else:
                    # COLLECTION case: change name given by user.
                    if tag == "<COLLECTION>":
                        tag = '<' + collectionName + '>'
                        xmlStringSimple += tag
                        stack.append(tag)

                    # Update xmlStringSimple
                    elif (tag == "<DATE>" or tag == "<TOPICS>" or
                       tag == "<PLACES>" or tag == "<PEOPLE>" or
                       tag == "<ORGS>" or tag == "<EXCHANGES>" or
                       tag == "<TEXT>" or tag == "<TITLE>" or
                       tag == "<AUTHOR>" or tag == "<DATELINE>" or
                       tag == "<BODY>" or tag == "<REUTERS>" or
                       tag == "<COLLECTION>"):

                        if tag == "<COLLECTION>":
                           tag = '<' + collectionName + '>'

                        xmlStringSimple += tag
                        stack.append(tag)

                    else:
                        tagContent = ""
                        print ("Tag not added: " + tag)
                #print (stack)

            # Already started parsing tag.
            else:
                # REUTERS case: only NEWID needed.
                if tag == "<REUTERS":
                    reutersContent += i

                else:
                    tag += i

        # Gets content of tag
        else:
            tagContent += i

    # Creates new simplified XML.
    fileName = ((filePath.split("\\")[-1]).split("."))[0]
    with open(fileName + "simpleXXX" + ".xml", 'w') as f:
        f.write(xmlStringSimple)

    parseXMLtoJSON(fileName + "simpleXXX" + ".xml")

    print(xmlStringSimple)


updateXML("C:\\Users\\Daniel\\Documents\\GitKraken\\XMLtoMongo\\reut2-000.xml", "ColeccionPrueba")

#parseXMLtoJSON("reut2-000simpleXXX.xml")
