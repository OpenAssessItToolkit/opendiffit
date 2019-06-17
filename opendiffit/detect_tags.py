from pdfminer3.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer3.pdfdevice import TagExtractor
from pdfminer3.pdfpage import PDFPage
from io import BytesIO

def convert_pdf(path, password=''):
    rsrcmgr = PDFResourceManager()
    retstr = BytesIO()
    try:
        try:
            device = TagExtractor(rsrcmgr, retstr, codec='utf-8')
        except:
            print('Not utf-8.')
        try:
            device = TagExtractor(rsrcmgr, retstr, codec='ascii')
        except:
            print('Not ascii.')
    except Exception as ex:
        print(ex)

    fp = open(path, 'rb')
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    maxpages = 1
    caching = True
    pagenos=set()
    for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password, caching=caching, check_extractable=True):
        interpreter.process_page(page)

    contents = retstr.getvalue().decode()
    fp.close()
    device.close()
    retstr.close()
    print(contents)

    # check if common proprietary Acrobat tags are in the response
    tags = ["<b\'Part\'", "</b\'Sect\'", "</b\'Art\'", "<b'Content'", "<b\'Artifact\'"]
    for tag in tags:
        if tag in contents:
            print('tagged')
            break
        else:
            continue


if __name__ == '__main__':
    import sys
    convert_pdf(sys.argv[1])

# python3 convert_pdf.py somefile.pdf