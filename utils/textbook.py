import requests
from libgen_api import LibgenSearch
import pdftotext

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
    s = LibgenSearch()
    results = s.search_title(textbook_name)
    item_to_download = results[0]
    download_links = s.resolve_download_links(item_to_download)
    url = download_links['GET']
    textbook = requests.get(url)
    f = open("test.pdf","wb")
    f.write(bytes(textbook.content))
    f.close()

    return convert_pdf_to_text("test.pdf")

def convert_pdf_to_text(textbook_path):
    """
    This method will produce text from a pdf file using OCR.
    :param textbook_path: path to textbook
    :type textbook_path: str
    :return: String object with pdf text
    """
    with open(textbook_path, "rb") as f:
        pdf = pdftotext.PDF(f)
    print(pdf)
    return "".join(list(pdf))

if __name__ == "__main__":
    print(convert_pdf_to_text(""))
    #pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    #convert_pdf_to_text("Financial-Strategy-for-Public-Managers-1628448595.pdf")
#%%
