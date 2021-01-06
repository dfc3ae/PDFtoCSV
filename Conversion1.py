import fitz
import pytesseract
import cv2
from PyPDF2 import PdfFileWriter, PdfFileReader, PdfFileMerger

pytesseract.pytesseract.tesseract_cmd = 'C://Program Files//Tesseract-OCR//tesseract.exe'
tessdata_dir_config = '--tessdata-dir "C://Program Files//Tesseract-OCR//tessdata"'


def rasterToPDF(page):
    bottomRight = [page.MediaBoxSize.x, page.MediaBoxSize.y]
    upperRight = [bottomRight[0], bottomRight[1]-300]
    upperLeft = [bottomRight[0]-300, bottomRight[1]-300]
    bottomLeft = [bottomRight[0]-300, bottomRight[1]]
    page = page.cropBox([bottomLeft, bottomRight, upperLeft, upperRight])
    pix = page.getPixmap()
    output = "outfile.png"
    pix.pillowWrite(output)
    img = cv2.imread("outfile.png", 1)
    result = pytesseract.image_to_pdf_or_hocr(img, extension='pdf', lang="eng", config=tessdata_dir_config)
    f = open("Resulting.pdf", "w+b")
    f.write(bytearray(result))
    f.close()
    pdf_file = fitz.open("Resulting.pdf")
    for pageNumber, page2 in enumerate(pdf_file.pages(), start=1):
        text = page2.getTextPage()
        text1 = text.extractBLOCKS()
    return text1

pdffile = fitz.open("vol-6.1.001-15-052-3.1-000-location-plan.pdf")

for pageNumber, page in enumerate(pdffile.pages(), start =1):
    rasterToPDF(page)
