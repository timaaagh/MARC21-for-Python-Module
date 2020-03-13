import MARC21

# converts byte values to strings and changes character values based on MARC spec
def data_toString(data):
    code = data["code"]
    
    indicators = data["indicators"].decode()
    indicators = indicators.replace(" ", "#") # blank indicators use '#' for readability
    
    dataField = data["data"].decode()
    dataField = dataField.replace("\x1f", "$") # replace delimiters for readability

    dataStr = code + " " + indicators + " " + dataField
    return dataStr

def isbn_toString(isbn):
    isbnStr = isbn.decode()
    isbnStr = isbnStr.strip()
    isbnStr = isbnStr[2:]  # strip delim and identifier off beginning
    return isbnStr

def title_toString(title, indicator):
    titleStr = title.decode()
    titleStr = titleStr.replace("\x1f", "$")
    titleStr = titleStr.strip()
    titleStr = titleStr[1:]  # strip delim off beginning

    indStr = indicator.decode()
    indStr = indStr.replace(" ", "#")

    titleStr += " {" + indStr + "}"
    return titleStr
    
    
    
# Main Scripts ---------------------------------------------------

# view all data fields in record
marcFile = open("AccessMedicineJanuary2020.mrc", "rb")
reader = MARC21.Reader(marcFile)
for record in reader:
    parser = MARC21.Parser(record)
    recordData = parser.get_data_list()
    for fieldData in recordData:
        print(data_toString(fieldData))
    print()
marcFile.close()


# view record ISBNs
##marcFile = open("AccessMedicineJanuary2020.mrc", "rb")
##reader = MARC21.Reader(marcFile)
##for record in reader:
##    parser = MARC21.Parser(record)
##    recordData = parser.get_data_list()
##    ISBNs = ""
##    title = ""
##    for fieldData in recordData:
##        if fieldData["code"] == "020":
##            ISBNs += isbn_toString(fieldData["data"])
##            ISBNs += "\n"
##        elif fieldData["code"] == "246":
##            title = title_toString(fieldData["data"], fieldData["indicators"])
##        else:
##            continue
##    print(title + "\n" + ISBNs)
##    print()
##marcFile.close()
