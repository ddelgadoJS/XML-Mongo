import json
import xmltodict
import re
import os
import MongoConnection as Conn

# Reads and parses an XML string to a JSON string, then inserts it to MongoDB.
# Code partially written by Alex.
# tripsintech.com/xml-to-json-python-script-also-json-to-xml/
def parseXMLtoJSON(database, collectionName, enhancedXMLString):
    jsonString = json.dumps(xmltodict.parse(enhancedXMLString).get("REUTERS"), indent=4)

    Conn.insertDocument(database, collectionName, json.loads(jsonString))

# Receives XML string.
# Returns last XML tag of given string.
# If there is no tag, prints an error and returns None
def getLastTag(xmlString):
    lastTag = "" # Variable to return the last tag.
    started = False # To check if started adding tag.

    # Reversed because the important is the final tag.
    for c in reversed(xmlString):
        # Didn't start reading tag, but final character of tag is on c (">").
        if started == False and c == '>':
            started = True
            lastTag = c

        # Currently reading tag and initial character of tag is on c ("<").
        # Here the reading has finished, return.
        elif started == True and c == '<':
            lastTag = c + lastTag
            return lastTag

        # Reading tag's name.
        elif started == True:
            # Added backwards because the string was reversed.
            lastTag = c + lastTag
    else:
        print ("No tag founded")
        return None

# Gets NEWID from <REUTERS> attribute.
# Receives all the attributes inside <REUTERS> as a string.
# Returns string "<NEWID> # </NEWID>".
def getNEWID(reutersContent):
    newid = "" # Variable to return the NEWID value.

    # Looks for NEWID starting at index of attribute.
    for i in range(reutersContent.find("NEWID"), len(reutersContent)):
        newid += reutersContent[i]

    # Gets NEWID value and removes quotes from value.
    newid = re.sub('[\"]', '', "<NEWID>" + newid.split("=")[-1] + "</NEWID>")

    return newid

# checkDTags() is called if the tag being read can have <D>.
# If tagContent only has one value, returns the same string.
def checkDTags(tagContent, openingTag, closingTag):
    # In case there are multiple elements inside tag.
    splittedTagContent = tagContent.split("</D>")

    # If tagContent has more than one value.
    if len(splittedTagContent) > 1:
        tagContent = ""

        for i in range(0, len(splittedTagContent) - 1):
            # First element, doesn't need openingTag.
            if i == 0:
                tagContent += splittedTagContent[i] + closingTag

            # Last element, doesn't need closingTag.
            elif i == len(splittedTagContent) - 2:
                tagContent += openingTag + splittedTagContent[i]

            # Middle elements, do need openingTag and closingTag.
            else:
                tagContent += openingTag + splittedTagContent[i] + closingTag

    return tagContent

# Deletes "COLLECTION" line and respective ending parenthesis.
# This is for the appropriate insert of document to MongoDB.
def deleteCollectionTag(fileName):
    with open(fileName + ".json", 'r') as f:
        jsonLines = f.readlines()

    enhancedJsonString = ""
    for i in range (0, len(jsonLines)):
        if i != 1 and i != len(jsonLines) - 2:
            enhancedJsonString += jsonLines[i]

    with open(fileName + ".json", 'w') as f:
        f.write(enhancedJsonString)

# Receives path to innacurate XML file.
# Returns path to enhanced XML file (makes a new one).
def enhanceXML(database, collectionName, directoryPath, innacurateXMLPath):
    articlesCount = 0 # Variable to increment the file name.

    with open(directoryPath + "\\" + innacurateXMLPath, 'r') as f:
        innacurateXMLString = f.read()

    stack = []
    tag = tagContent = reutersContent = enhancedXMLString = completeEnhancedXMLString = ""

    for token in innacurateXMLString:
        # Checks that stack has at least one element to avoid error on next condition.
        # If stack[-1] == '<' a tag is being read.
        if token == '<' or (len(stack) > 0 and stack[-1] == '<'):
            # Start of file or tag's start.
            if len(stack) == 0 or stack[-1] != '<':
                # Token is '<'.
                tag = token
                stack.append(token) # Adds '<' to know it's parsing a tag.

            # Tag's end.
            elif token == '>':
                stack.pop() # Pops '<', it's no longer parsing a tag.
                tag += token # Adds closing token of tag.

                if tag[1] == '/':
                    if (tag == "</DATE>" or tag == "</TOPICS>" or
                        tag == "</PLACES>" or tag == "</PEOPLE>" or
                        tag == "</ORGS>" or tag == "</EXCHANGES>" or
                        tag == "</TEXT>" or tag == "</TITLE>" or
                        tag == "</AUTHOR>" or tag == "</DATELINE>" or
                        tag == "</BODY>" or tag == "</REUTERS>" or
                        tag == "</D>"):

                        # This means this tagContent needs to be processed.
                        if tag == "</D>":
                            # Adds tag at the end of each element as character
                            #  of control to know how to divide the string.
                            tagContent += tag

                        else:
                            # Checks if tagContent is separated by <D>.
                            tagContent = checkDTags(tagContent, stack[-1], tag)
                            enhancedXMLString += tagContent
                            tagContent = ""

                            # If closing tag is already written won't add it.
                            # This can happens with </D>.
                            if getLastTag(enhancedXMLString) != tag:
                                enhancedXMLString += tag

                            # If end of article, insert it to database.
                            if tag == "</REUTERS>":
                                parseXMLtoJSON(database, collectionName, enhancedXMLString)
                                completeEnhancedXMLString += enhancedXMLString
                                enhancedXMLString = ""

                        # Checks that stack has at least one element
                        #  to avoid error on next condition.
                        # If top stack tag is the opening tag of
                        #  currently tag, pop it.
                        if len(stack) > 0 and stack[-1] == tag[0] + tag[2:]:
                            stack.pop() # Pops opening tag.

                        # Opening tag not found, this is not an error.
                        else:
                            pass
                            #print ("Opening tag not found: " + tag)

                    # Tag content not added, this is not an error.
                    # In case the tag is not important.
                    else:
                        tagContent = ""
                        #print ("Tag not added: " + tag)

                # First line of file ignored, this is not an error.
                elif tag[1] == '?':
                    pass
                    #print ("First line ignored.")

                else:
                    if (tag == "<DATE>" or tag == "<TOPICS>" or
                        tag == "<PLACES>" or tag == "<PEOPLE>" or
                        tag == "<ORGS>" or tag == "<EXCHANGES>" or
                        tag == "<TEXT>" or tag == "<TITLE>" or
                        tag == "<AUTHOR>" or tag == "<DATELINE>" or
                        tag == "<BODY>" or tag == "<REUTERS>" or
                        tag == "<D>"):

                        # Process as a normal tag, without <D>
                        if tag != "<D>":
                            enhancedXMLString += tag
                            stack.append(tag)

                            # Gets and adds NEWID attribute.
                            if tag == "<REUTERS>":
                                enhancedXMLString += getNEWID(reutersContent)
                                reutersContent = ""

                    # Tag content not added, this is not an error.
                    # In case the tag is not important.
                    else:
                        tagContent = ""
                        #print ("Tag not added: " + tag)

            # Currently parsing a tag.
            else:
                # REUTERS case: only NEWID needed.
                if tag == "<REUTERS":
                    reutersContent += token

                # TEXT case: tag with attributes.
                elif tag == "<TEXT":
                    if token == '>':
                        tag += token

                # Normal tag parsing.
                else:
                    tag += token

        # Gets content of tag
        else:
            # Removes weird tokens.
            if token == '&':
                tagContent += 'and'
            elif token == '#':
                tagContent += 'hash'
            # Parses normal token.
            else:
                tagContent += token

    if not os.path.exists("JSONs"):
        os.makedirs("JSONs")

    # Adds <COLLECTION> tags to avoid error when parsing to JSON.
    completeEnhancedXMLString = "<COLLECTION>" + completeEnhancedXMLString + "</COLLECTION>"
    jsonString = json.dumps(xmltodict.parse(completeEnhancedXMLString), indent=4)

    # Creates JSON file of enhanced XML file.
    innacurateFileName = ((innacurateXMLPath.split("\\")[-1]).split("."))[0]
    with open("JSONs\\" + innacurateFileName + ".json", 'w') as f:
        f.write(jsonString)
