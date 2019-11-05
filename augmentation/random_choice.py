import os
import numpy as np
from glob import glob
import shutil
import random


def main():
    export = 'unknown/Noise'
    if not os.path.exists(export):
        os.makedirs(export)

    img_list = []

    target = 'Images/Noise/*'
    for f in glob(target):
        img_list.append(f)

    test_num = 320
    xs = random.sample(img_list, test_num)
    print(xs)

    for x in xs:
        shutil.move(x, export)


if __name__ == '__main__':
    main()
