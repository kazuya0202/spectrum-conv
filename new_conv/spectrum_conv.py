from pydub import AudioSegment
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

import os
import sys
import glob
from PIL import Image


class Util:
    def __init__(self):
        # conv()
        # 画像出力先ディレクトリ
        self.export_dir = 'spectrum-img'

        # crop()
        # 画像の切り取り範囲
        self.crop_range = (169, 58, 487, 427)

        # 切り取るかどうか
        self.is_crop = True

    def make_dirs(self, dir_name):
        """指定したディレクトリが存在しなければディレクトリを作成"""
        if not self.is_exists(dir_name):
            os.makedirs(dir_name)

    def is_exists(self, dir_name):
        """ファイル, ディレクトリが存在するかどうか"""
        return os.path.exists(dir_name)

    def splitext(self, path):
        """拡張子で区切る"""
        return os.path.splitext(path)

    def get_fname(self, path):
        """ファイル名のみを取得"""
        fname = self.splitext(path)[0]
        return fname

    def get_ext(self, path):
        """拡張子のみを取得"""
        ext = self.splitext(path)[1][1:]
        return ext

    def load_wav(self, wav_path):
        """wavファイルを読み込む"""
        # 読み込み
        sound = AudioSegment.from_wav(wav_path)

        # サンプルデータ取得
        samples = np.array(sound.get_array_of_samples())
        sample = samples[::sound.channels]
        sound._data = sample

        return sound


class SpectrumConvertion:
    def __init__(self):
        self.util = Util()

        self.export_dir = self.util.export_dir
        self.crop_range = self.util.crop_range

        self.file_path = ''

        # 音データ
        self.sound = None

    def conv(self):
        print(self.file_path)
        self.sound = self.util.load_wav(self.file_path)

    def crop(self):

        pass

    def main(self):
        argv = sys.argv

        # self.file_path = argv[1] if len(argv) >= 2 \
        #     else input('> Enter file path: ')
        if len(argv) >= 2 and (argv[1] == '-h' or argv[1] == '--help'):
            print('Usage:')
            print('  python <this-file>.py **/*.wav')
            print('  python <this-file>.py <audio_file>.wav')
            print('  python <this-file>.py')

            exit()
            # return

        if len(argv) == 1:
            fpath = input('> Enter file path: ')
            argv.append(fpath)

        # script.py は無視するために it = 1
        argv_len = len(argv)
        it = 1

        while (it < argv_len):
            self.file_path = argv[it]

            # 存在しないなら continue
            if not self.util.is_exists(self.file_path):
                continue

            # print(self.file_path)
            # 変換
            self.conv()

            # 切り取るなら
            if self.util.is_crop:
                self.crop()

            it += 1


if __name__ == '__main__':
    sc = SpectrumConvertion()
    sc.main()
