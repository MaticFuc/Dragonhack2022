import requests
import pytesseract
from pdf2image import convert_from_path

#
# This file is for processing textbook PDFs using OCR
# If this is not possible it will return an Error
#

def find_textbook(textbook_name):
    """
    Tries to find a textbook in a specific website. If it finds it, it will download the first one.
    :param textbook_name:
    :type textbook_name: str
    :return:
    """
    id = ""
    url = "https://open.umn.edu/opentextbooks/textbooks.json"
    textbooks = requests.get(url, params={'term':textbook_name, 'page':1}).json()["data"]
    for textbook in textbooks:
        formats = textbook["formats"]
        for format in formats:
            if format["format"] == "PDF":
                id = format["id"]
                url = format["url"]
        if id != "":
            break
    #url = "https://open.umn.edu/opentextbooks/formats/" + str(id)
    textbook = requests.get(url)
    return textbook

def convert_pdf_to_text(textbook_path):
    """
    This method will produce text from a pdf file using OCR.
    :param textbook_path: path to textbook
    :type textbook_path: str
    :return: String object with pdf text
    """
    pages = convert_from_path(textbook_path, 5)
    file = open("result" + ".txt","w")
    for pageNum, imgBlob in enumerate(pages):
        text = pytesseract.image_to_string(imgBlob, lang='eng')
        file.write(text)
    file.close()

if __name__ == "__main__":
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    convert_pdf_to_text("Financial-Strategy-for-Public-Managers-1628448595.pdf")
