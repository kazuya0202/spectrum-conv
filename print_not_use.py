import os
from glob import glob


def main():
    img_name = []
    for f in glob('./spectrum-save-img/_Crossing/*.jpg'):
        x = os.path.basename(f)
        x = os.path.splitext(x)[0]
        img_name.append(x)
    # print(len(img_name))

    for f in glob('./export/wav/crossing-samp1/*'):
        x = os.path.basename(f)
        x = os.path.splitext(x)[0]
        if x not in img_name:
            print(x)
            os.remove(f)
            pass


if __name__ == "__main__":
    main()
