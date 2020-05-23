import os
import io
import PyPDF2
from PIL import Image

"""
pip install PyPDF2
"""


def pdf_image_extractor(pdffile, page=None, pages=None, return_array_list=False):
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
        if pages[1] == -1:
            pages = range(pages[0], pdf.getNumPages())
        else:
            pages = range(pages[0], pages[1])
    pdfpath_without_ext = os.path.join(os.path.dirname(pdffile), os.path.splitext(os.path.basename(pdffile))[0])
    img_array_list = []
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
                except NotImplementedError:
                    data = xObject[obj]._data  # じゃないとだめなこともある？
                if xObject[obj]['/ColorSpace'] == '/DeviceRGB':
                    mode = "RGB"
                else:
                    mode = "P"

                file_name_without_ext = f"{pdfpath_without_ext}_{page}_{obj[1:]}"
                if '/Filter' in xObject[obj]:
                    if xObject[obj]['/Filter'] == '/FlateDecode':
                        img = Image.frombytes(mode, size, data)
                        if return_array_list:
                            img_array_list.append(img)
                        else:
                            img.save(file_name_without_ext + ".png")
                    elif xObject[obj]['/Filter'] == '/DCTDecode':
                        if return_array_list:
                            img_array_list.append(Image.open(io.BytesIO(data)))
                        else:
                            img = open(file_name_without_ext + ".jpg", "wb")
                            img.write(data)
                            img.close()
                    elif xObject[obj]['/Filter'] == '/JPXDecode':
                        if return_array_list:
                            img_array_list.append(Image.open(io.BytesIO(data)))
                        else:
                            img = open(file_name_without_ext + ".jp2", "wb")
                            img.write(data)
                            img.close()
                    elif xObject[obj]['/Filter'] == '/CCITTFaxDecode':
                        if return_array_list:
                            img_array_list.append(Image.open(io.BytesIO(data)))
                        else:
                            img = open(file_name_without_ext + ".tiff", "wb")
                            img.write(data)
                            img.close()
                    else:
                        if xObject[obj]['/Filter'] == ['/FlateDecode']:
                            img = Image.frombytes(mode, size, data)
                            if return_array_list:
                                img_array_list.append(img)
                            else:
                                img.save(file_name_without_ext + ".png")
                        else:
                            print(xObject[obj]['/Filter'])
                else:
                    img = Image.frombytes(mode, size, data)
                    if return_array_list:
                        img_array_list.append(img)
                    else:
                        img.save(file_name_without_ext + ".png")
    if return_array_list:
        return img_array_list
    print("Done!")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('filepath')
    parser.add_argument('-p', '--page', type=int, default=None)
    parser.add_argument('-ps', '--pages', type=int, nargs=2, default=None)
    parser.add_argument('-ar', '--array_list', action='store_true')
    args = parser.parse_args()
    pdf_image_extractor(args.filepath, args.page, args.pages, args.array_list)
