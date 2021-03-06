# authors: Dennis Chiappetta and Jen Gulley
# uses PyMuPDF library
import re
import fitz
import csv

def pdfToCSV(file):
    """
    main function for creating csv file from pdf
    :param file: the pdf file to open and convert to csv
    :return: none; creates csv file with the same as the pdf file
    """
    # create csv file
    csvFile = open("csvFile.csv", 'w')

    # get the csv filename from the pdf filename
    csvFilename = file[0:-3]
    csvFilename = csvFilename + "csv"

    # make header for csv
    header = "page_number,x0,y0,x1,y1,text,page_drawing_no\n"
    csvFile.write(header)
    csvFile.close()

    # open the pdf
    pdf_file = fitz.open(file)


    # for loop going into each page
    for pageNumber, page in enumerate(pdf_file.pages(), start=1):
        csvFile = open("csvFile.csv", 'a', encoding='utf-8')
        # makes in textpage
        text = page.getTextPage()
        # call to method in library that gets all necessary information
        text1 = text.extractBLOCKS()
        # call to method in library that gets all images (raster PDFs?)
        # text2 = page.getImageList()
        # goes through the list of items in text1 because text1 is list of lists
        pageSize = page.MediaBoxSize
        xSize = pageSize.x
        ySize = pageSize.y
        for each in text1:
            # reformats text
            eachText = str(each[4]).replace("\n", " ").replace("\"", "'""'")
            # write to csv with call to regex
            csvFile.write((str(pageNumber) + "," + str(each[0]) + "," + str(each[1]) + "," + str(each[2]) + "," +
                           str(each[3]) + ","
                      + "\"" + eachText + "\"" + "," + coordMatch(each[0], each[1], xSize, ySize, eachText) + "\n"))
        # for piece in text2:
        #     # insert raster to vector method here
        #     csvFile.write(str(pageNumber) + "," + str(piece[0]) + "," + str(piece[1]) + "," + str(piece[2]) + "," +
        #             str(piece[3]) + ",image: " + str(piece[7]) + "\n")
        csvFile.close()

    # add a new column to the csv called page_drawing_no which tells you whether the drawing number
    # is the drawing number of the page
    myCsv = csv.reader(open("csvFile.csv", encoding='utf-8'))
    csvFileFinal = open(csvFilename, 'w', encoding='utf-8')
    row0 = next(myCsv)
    # header for the new column
    row0.append("contains_drawing_no\n")
    row0 = listToString(row0)
    csvFileFinal.write(row0)
    # for loop to go through each row in original csv and add a new column in updated csv
    for row in myCsv:
        row[5] = "\"" + row[5] + "\""
        row.append(drawingNo(row[5]) + "\n")
        rowString = listToString(row)
        csvFileFinal.write(rowString)
    csvFileFinal.close()

def drawingNo(text):
    """
    regex function to find all drawing numbers
    :param text: string to be searched for drawing number
    :return: boolean as a string; returns true if the text contains a drawing number, false otherwise
    """
    # starting value of boolean
    boolean = False
    for each in drawingNoList:
        if each in text:
            boolean = True
    return str(boolean)


drawingNoList = []

def coordMatch(x, y, xSize, ySize, text):
    """
    takes in x and y coordinates and determines if they match the x and y coordinates of interest
    :param x: float, x coordinate
    :param y: float, y coordinate
    :param xSize: float, 
    :return: boolean as a string; returns true if the coordinates match, false otherwise
    """
    pattern = r"\b[a-zA-Z]{1,3}[1-9]{0,3}\s?[.-]?\s?[0-9]{1,4}[.-_]?[a-zA-Z0-9]{1,3}\b(?<!\d\d\d\d\d)"
    reg = re.compile(pattern)
    boolean = False
    if y > ySize-300 and x > xSize-300:
        if reg.search(text):
            boolean = True
            text = text.replace(" ", "")
            drawingNoList.append(text)
            #print(drawingNoList)
    return str(boolean)

def listToString(listToConvert):
    """
    takes in a list and converts it to a string separated by commas
    :param listToConvert: list to be converted
    :return: string separated by commas
    """
    s = ""
    for each in listToConvert:
        s = s + each + ","
    s = s[0:-1]
    return s

pdfToCSV("20170814_PVL-Bid-Set-1P1-19.pdf")

