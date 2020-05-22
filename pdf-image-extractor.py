import PyPDF2
from PIL import Image

"""
pip install PyPDF2
"""

def main(pdffile, page=None, pages=None):
    if page is None and pages is None:
        raise ValueError
    if page is not None and pages is not None:
        raise ValueError
    pdf = PyPDF2.PdfFileReader(open(pdffile, "rb"))
    if page is not None:
        if type(page) != int:
            raise TypeError(page)
        pages = [page]
    elif pages is not None:
        pages = range(pages[0], pages[1])
    for page in pages:
        this_page = pdf.getPage(page)

        if '/XObject' not in this_page['/Resources']:
            print(f"XObject does not exist in page {page}")
            continue

        xObject = this_page['/Resources']['/XObject'].getObject()
        for obj in xObject:
            if xObject[obj]['/Subtype'] == '/Image':
                size = (xObject[obj]['/Width'], xObject[obj]['/Height'])
                try:
                    data = xObject[obj].getData()
                except:
                    data = xObject[obj]._data  # じゃないとだめなこともある？
                if xObject[obj]['/ColorSpace'] == '/DeviceRGB':
                    mode = "RGB"
                else:
                    mode = "P"
        
                if '/Filter' in xObject[obj]:
                    if xObject[obj]['/Filter'] == '/FlateDecode':
                        img = Image.frombytes(mode, size, data)
                        img.save(obj[1:] + ".png")
                    elif xObject[obj]['/Filter'] == '/DCTDecode':
                        img = open(obj[1:] + ".jpg", "wb")
                        img.write(data)
                        img.close()
                    elif xObject[obj]['/Filter'] == '/JPXDecode':
                        img = open(obj[1:] + ".jp2", "wb")
                        img.write(data)
                        img.close()
                    elif xObject[obj]['/Filter'] == '/CCITTFaxDecode':
                        img = open(obj[1:] + ".tiff", "wb")
                        img.write(data)
                        img.close()
                else:
                    img = Image.frombytes(mode, size, data)
                    img.save(obj[1:] + ".png")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('filepath')
    parser.add_argument('-p', '--page', type=int, default=None)
    parser.add_argument('-ps', '--pages', type=int, nargs=2, default=None)
    args = parser.parse_args()
    main(args.filepath, args.page, args.pages)
