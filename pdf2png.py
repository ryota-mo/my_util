import argparse
from pathlib import Path
from pdf2image import convert_from_path

"""
pip install pdf2image
"""


def main(pdfpath, dpi=300):
    pdfpath = Path(pdfpath)
    image = convert_from_path(pdfpath, dpi)
    if len(image) == 1:
        pngpath = pdfpath.parent.resolve() / (pdfpath.stem + '.png')
        if pngpath.is_file():
            raise FileExistsError(str(pngpath))
        image[0].save(pngpath, 'png')
    else:
        for i in range(len(image)):
            pngpath = pdfpath.parent.resolve() / (pdfpath.stem + f'_{i}.png')
            if pngpath.is_file():
                raise FileExistsError(str(pngpath))
            image[i].save(pngpath, 'png')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('pdfpath')
    parser.add_argument('--dpi', type=int, default=300, help="defualt: 300")
    args = parser.parse_args()
    main(args.pdfpath, args.dpi)
