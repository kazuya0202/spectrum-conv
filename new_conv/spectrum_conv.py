from os.path import exists
from pydub import AudioSegment
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

import os
import sys
import glob
from PIL import Image

from pathlib import Path
from sys import path

from utils import Utils
from global_variables import GlobalVariables


class SpectrumConvertion:
    def __init__(self):
        self.ul = Utils()
        self.gv = GlobalVariables()

        self.path = Path('')

        # 音データ
        self.sound = None

        if self.gv.is_wav_save:
            Path.mkdir(self.gv.wav_export)

    def conv_and_plot(self):
        print(self.path)

        # load file
        self.sound = self.ul.load_wav(self.path)
        self.sample = self.sound._data

        """ スペクトログラム作成 """
        w = 1000  # 窓枠
        s = 500  # 刻み

        ampList = []  # スペクトル格納用
        argList = []  # 偏角格納用

        i = None
        data = None

        # 刻みずつずらしながら窓幅分のデータをフーリエ変換
        for i in range(int((self.sample.shape[0] - w) / s)):
            data = self.sample[i * s:i * s + w]
            spec = np.fft.fft(data)
            spec = spec[:int(spec.shape[0] / 2)]
            spec[0] = spec[0] / 2
            ampList.append(np.abs(spec))
            argList.append(np.angle(spec))

        # 周期数は共通なので1回だけ計算（縦軸表示に使う）
        freq = np.fft.fftfreq(data.shape[0], 1.0 / self.sound.frame_rate)
        freq = freq[:int(freq.shape[0] / 2)]

        # 時間も共通なので1回だけ計算（横軸表示に使う）
        time = np.arange(0, i + 1, 1) * s / self.sound.frame_rate

        # numpyの配列にする
        ampList = np.array(ampList)
        argList = np.array(argList)

        # seaborn の heatmap を使う
        plt_data = pd.DataFrame(data=ampList, index=time, columns=freq)
        sns.heatmap(data=np.log(plt_data.iloc[:, :100].T),
                    xticklabels=False,
                    yticklabels=False,
                    cbar=False,
                    cmap=plt.cm.gist_rainbow_r,
                    vmin=1,
                    square=True)

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

        # script.py は無視するために it は 1 から
        argv_len = len(argv)
        it = 1

        # while (it < argv_len):
        for i, wav_file in enumerate(argv):
            # ignore <script>.py
            if i == 0:
                continue

            # self.file_path = Path(argv[it])
            self.path = Path(wav_file)

            # 存在しないなら continue
            if not self.path.exists():
                # it += 1
                continue

            fname = self.path.stem
            ext = self.path.suffix

            # wav ファイルでないなら continue
            # if self.ul.get_ext(self.file_path) != 'wav':
            if ext != '.wav':
                print('not wav.')
                # it += 1
                continue

            # print(self.file_path)
            # 変換
            self.conv_and_plot()

            # self.path.parent
            # self.path.joinpath()
            wav_export_dir = Path(self.gv.wav_export).joinpath(self.path.parent)
            print(wav_export_dir)

            p = wav_export_dir.joinpath(f'{fname}_{i}.wav')
            print(p)

            if self.gv.is_save:
                plt.savefig(fname)

            # 切り取るなら
            if self.gv.is_crop:
                self.ul.crop(self.gv.crop_range)

            # it += 1

        return 0


if __name__ == '__main__':
    sc = SpectrumConvertion()
    exit_status = sc.main()

    sys.exit(exit_status)
