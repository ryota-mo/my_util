import argparse
from pathlib import Path
from pdf2image import convert_from_path

"""
pip install pdf2image
"""


def main(pdfpath, dpi=300, is_jpg=False):
    ext = "jpg" if is_jpg else "png"
    pdfpath = Path(pdfpath)
    image = convert_from_path(pdfpath, dpi)
    if len(image) == 1:
        pngpath = pdfpath.parent.resolve() / (pdfpath.stem + f'.{ext}')
        if pngpath.is_file():
            raise FileExistsError(str(pngpath))
        image[0].save(pngpath)
    else:
        for i in range(len(image)):
            pngpath = pdfpath.parent.resolve() / (pdfpath.stem + f'_{i}.{ext}')
            if pngpath.is_file():
                raise FileExistsError(str(pngpath))
            image[i].save(pngpath)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('pdfpath')
    parser.add_argument('--dpi', type=int, default=300, help="default: 300")
    parser.add_argument('-j', '--jpg', action="store_true", help="output jpg")
    args = parser.parse_args()
    main(args.pdfpath, args.dpi, is_jpg=args.jpg)
