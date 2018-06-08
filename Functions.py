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
def parseXMLtoJSON(filePath, collectionName):
    filePath = updateXML(filePath, collectionName)

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

# Returns last tag of given string.
def getLastTag(xmlString):
    lastTag = ""
    started = False # Checks if started adding tag '>'
    for c in reversed(xmlString):
        if started == False and c == '>':
            started = True
            lastTag = c

        elif started == True and c == '<':
            lastTag = c + lastTag
            return lastTag

        elif started == True:
            lastTag = c + lastTag
    else:
        print ("No tag founded")

def checkDTags(tagContent, openingTag, closingTag):
    # In case there are multiple elements inside tag.
    splittedTagContent = tagContent.split("</D>")
    if len(splittedTagContent) > 1:
        tagContent = ""
        for i in range(0, len(splittedTagContent) - 1):
            # First element, doesn't need openingTag.
            if i == 0:
                tagContent += splittedTagContent[i] + closingTag

            # Last element, doesn't need closingTag.
            elif i == len(splittedTagContent) - 2:
                tagContent += openingTag + splittedTagContent[i]

            else:
                tagContent += openingTag + splittedTagContent[i] + closingTag

    """elif  len(splittedTagContent) == 1 and (
          openingTag == "<TOPICS>" or openingTag == "<PLACES>" or
          openingTag == "<PEOPLE>" or openingTag == "<ORGS>" or
          openingTag == "<EXCHANGES>"):
          # Because this tags can have multiple fields this must be an array in JSON.
          tagContent = openingTag + tagContent + closingTag
          print (tagContent)"""

    return tagContent

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
                       tag == "</COLLECTION>" or tag == "</D>"):

                        # COLLECTION case: change name given by user.
                        if tag == "</COLLECTION>":
                            tag = '</' + collectionName + '>'

                        elif tag == "</D>":
                            tagContent += tag

                        """elif tag == "</TITLE>":
                            # Inside <TITLE> are some weird characters.
                            # It's necessary to remove them.
                            tagContent = tagContent[5:]

                        elif tag == "</BODY>":
                            # Inside <BODY> are some weird characters.
                            # It's necessary to remove them.
                            tagContent = tagContent[:-4]
                        """

                        """elif tag == "</D>":
                            # <D> CASE, multiple elements inside tag.
                            # If in original XML is like this:
                            #   <PLACES><D>el-salvador</D><D>usa</D></PLACES>
                            # It needs to be like this in simplified:
                            #   <PLACES>el-salvador</PLACES><PLACES>usa</PLACES>

                            # Checks if openingTag is already in xmlStringSimple.
                            endingTag = stack[-1][0] + '/' + stack[-1][1:] + stack[-1]
                            xmlStringSimple += tagContent + endingTag
                            tagContent = """

                        if tag != "</D>":
                            tagContent = checkDTags(tagContent, stack[-1], tag)
                            xmlStringSimple += tagContent
                            tagContent = ""

                            if getLastTag(xmlStringSimple) != tag:
                                xmlStringSimple += tag

                        if len(stack) > 0 and stack[-1] == tag[0] + tag[2:]: # Looks for ending tag in stack.
                            stack.pop() # Pops opening tag.

                        else:
                            print ("Opening tag not found: " + tag)

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
                       tag == "<COLLECTION>" or tag == "<D>"):

                        if tag == "<COLLECTION>":
                           tag = '<' + collectionName + '>'

                        if tag != "<D>":
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

                # TEXT case: tag with attributes.
                elif tag == "<TEXT":
                    if i == '>':
                        tag += i

                else:
                    tag += i

        # Gets content of tag
        else:
            if i == '&':
                tagContent += 'and'
            elif i == '#':
                tagContent += 'hash'
            else:
                tagContent += i

    # Creates new simplified XML.
    fileName = ((filePath.split("\\")[-1]).split("."))[0]
    with open(fileName + "_updated" + ".xml", 'w') as f:
        f.write(xmlStringSimple)

    return fileName + "_updated" + ".xml"
    #parseXMLtoJSON(fileName + "simpleXXX" + ".xml")

    #print(xmlStringSimple)

#updateXML("C:\\Users\\Daniel\\Documents\\GitKraken\\XMLtoMongo\\reut2-002.xml", "ColeccionPrueba")

#getLastTag("<xmlStringSimple>")

#parseXMLtoJSON("reut2-000.xml")
