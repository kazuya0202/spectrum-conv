import os
import sys
import spectrum_conv as sc


target_dir = 'export'


def main():
    argv = sys.argv
    fname = 'crossing1'
    if len(argv) >= 2:
        fname = argv[1]

        if fname.find('.') > -1:
            fname = fname[:fname.find('.')]
            fname += '/'

    path = f'{target_dir}/{fname}'
    if not os.path.exists(path):
        print(f'there is not {path}')
        sys.exit(-1)

    sc.main(path=path)
    # call(f'python spectrum-conv.py {path}')
    # for (root, dirs, files) in os.walk(path):
    #     for f in files:
    #         # print(f'{target_dir}/{f}')
    #         arg = f'{root}/{f}'
    #         call(f'python spectrum-conv.py {arg}')

    # print(fname)
    # print('main')


if __name__ == '__main__':
    main()
