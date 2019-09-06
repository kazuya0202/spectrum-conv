import os
import sys
import subprocess


def main():
    L = [
        'https://youtu.be/TLLLDXn8-9I',
        'https://youtu.be/q9qmSFn5GZc',
        'https://youtu.be/pYMl9leb_9I',
        'https://youtu.be/gziH2uxjmWw',
        'https://youtu.be/IO65kr_Lyrs',
        'https://youtu.be/75VxWrkFT1Q',
        'https://youtu.be/9HKL_8LVdyE',
        'https://youtu.be/KrUBrZcr_UI',
        'https://youtu.be/HVMorhj6Luo',
        'https://youtu.be/QZyvFpvw-nk',
        'https://youtu.be/5VIDQssbaW4',
        'https://youtu.be/4CBPouKVazs',
        'https://youtu.be/xmLgmhfuor0',
        'https://youtu.be/TsgxHNFxTeU',
        'https://youtu.be/IydSCSDoOl8',
        'https://youtu.be/Xzh7vLudwUw'
    ]

    for i in L:
        subprocess.call(f'youtube-dl {i}')


if __name__ == '__main__':
    main()
