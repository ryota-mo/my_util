import argparse
import os

import cv2
import numpy as np


def main(filepath):
    im = cv2.imread(filepath)
    height, width, _ = im.shape
    im_base = np.zeros((height, int(height * 1.5), 3))
    width_base = im_base.shape[1]
    im_base[:, (width_base - width) // 2 : (width_base - width) // 2 + width] = im
    cv2.imwrite("yoko_" + os.path.basename(filepath), im_base)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("filepath")
    args = parser.parse_args()
    main(args.filepath)
