import os
import sys
import cv2

# BBox形式で画像全体をアノテーションファイルを作る


def get_target_dir():
    argv = sys.argv

    dir_path = argv[1] if len(argv) >= 2 else 'c1'

    if not os.path.exists(dir_path):
        print('is not exist')
        sys.exit(-1)

    if not os.path.isdir(dir_path):
        print('is not directory')
        sys.exit(-1)

    # main(dir_path)
    return dir_path


def main(path):
    slash_location = path.rfind('/')

    # 末尾に/がある場合はdirname(path)
    p = os.path.dirname(path) if (slash_location == (len(path) - 1)) else path
    parent_dir = p[p.rfind('/') + 1:]

    output_path = f'annotated/{parent_dir}'

    if not os.path.exists(output_path):
        os.makedirs(output_path)

    for (root, dirs, files) in os.walk(path):
        for f in files:
            # load file
            im = cv2.imread(f'{root}/{f}')

            # get size
            shape = im.shape

            # output image
            cv2.imwrite(f'{output_path}/{f}', im)

            # yolo
            # classes | x_center | y_center | width | height
            # write_content = f'1 {shape[0] / 2} {shape[1] / 2} 1.0 1.0'

            # darknet-toolsを使うためBBox形式にする
            write_content = f'1\n0 0 {shape[0]} {shape[1]}\n'

            # remove extension of file
            txt_file = str(f[:f.find('.')]) + '.txt'

            # output annotation txt
            with open(f'{output_path}/{txt_file}', 'w') as txt:
                txt.write(write_content)

            print(f'  saved {f} / {txt_file}')


if __name__ == '__main__':
    path = get_target_dir()
    main(path)
