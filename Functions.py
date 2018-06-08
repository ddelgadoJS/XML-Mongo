import json
import xmltodict
import re

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
    filePath = updateXML(filePath)

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

# Gets NEWID from <REUTERS> attribute.
# Returns <NEWID> # </NEWID>
def getNEWID(reutersContent):
    newid = ""
    started = False # Checks if started adding attribute NEWID

    # Looks for NEWID starting at index of attribute.
    for i in range(reutersContent.find("NEWID"), len(reutersContent)):
        newid += reutersContent[i]

    # Gets value and prepare string
    newid = "<NEWID>" + newid.split("=")[-1] + "</NEWID>"

    # Returns id without quotes ("").
    return re.sub('[\"]', '', newid)

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

    return tagContent

def updateXML(filePath):
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

                        if tag == "</D>":
                            tagContent += tag

                        else:
                            tagContent = checkDTags(tagContent, stack[-1], tag)
                            xmlStringSimple += tagContent
                            tagContent = ""

                            # If closing tag is already written won't add it.
                            # This can happens with </D>.
                            if getLastTag(xmlStringSimple) != tag:
                                xmlStringSimple += tag

                        if len(stack) > 0 and stack[-1] == tag[0] + tag[2:]: # Looks for ending tag in stack.
                            stack.pop() # Pops opening tag.

                        else:
                            pass
                            #print ("Opening tag not found: " + tag)

                    else:
                        tagContent = ""
                        #print ("Tag not added: " + tag)

                # First line case.
                elif tag[1] == '?':
                    pass
                    #print ("First line ignored.")

                else:
                    # Update xmlStringSimple
                    if (tag == "<DATE>" or tag == "<TOPICS>" or
                       tag == "<PLACES>" or tag == "<PEOPLE>" or
                       tag == "<ORGS>" or tag == "<EXCHANGES>" or
                       tag == "<TEXT>" or tag == "<TITLE>" or
                       tag == "<AUTHOR>" or tag == "<DATELINE>" or
                       tag == "<BODY>" or tag == "<REUTERS>" or
                       tag == "<COLLECTION>" or tag == "<D>"):

                        if tag != "<D>":
                            xmlStringSimple += tag
                            stack.append(tag)

                            # Getting NEWID attribute.
                            if tag == "<REUTERS>":
                                xmlStringSimple += getNEWID(reutersContent)
                                reutersContent = ""

                    else:
                        tagContent = ""
                        #print ("Tag not added: " + tag)

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
