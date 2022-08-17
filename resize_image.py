import argparse
import os
from glob import glob

from PIL import Image


def resize_image(input_path, output_path, quality):
    im = Image.open(input_path)
    im.save(output_path, quality=quality)


def main(input_path, output_path, quality):
    assert 0 <= quality <= 95, quality
    if os.path.isdir(input_path):
        if not os.path.isdir(output_path):
            raise ValueError(output_path)
        image_paths = (
            glob(os.path.join(input_path, "*.JPG"), recursive=True)
            + glob(os.path.join(input_path, "*.jpg"), recursive=True)
            + glob(os.path.join(input_path, "*.png"), recursive=True)
        )
        for _image_path in image_paths:
            resize_image(
                _image_path,
                os.path.join(output_path, os.path.basename(_image_path)),
                quality,
            )
    elif os.path.isfile(input_path):
        resize_image(input_path, output_path, quality)
    else:
        raise ValueError(input_path)


def main0(input_path, output_path, dpi: int = 300):
    im = Image.open(input_path)
    im.save(output_path, dpi=(dpi, dpi))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input_path")
    parser.add_argument("output_path")
    parser.add_argument("quality", type=int)
    args = parser.parse_args()
    main(args.input_path, args.output_path, args.quality)
