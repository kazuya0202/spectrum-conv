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

# from utils import Utils
import utils as ul
from global_variables import GlobalVariables
from separate_wav import SeparateWav


class SpectrumConvertion:
    def __init__(self):
        # ul = Utils()
        self.gv = GlobalVariables()
        self.sw = SeparateWav()

        self.path = Path('')

        # 音データ
        self.sound = None
        self.sample = None

        self.wav_exp_base = Path(self.gv.wav_exp_dir)
        self.img_exp_base = Path(self.gv.img_exp_dir)
        # self.it = 0

        if self.gv.is_save_wav:
            wav_exp_dir = Path(self.gv.wav_exp_dir)
            Path.mkdir(wav_exp_dir)

    def conv_and_plot(self, wav_data=None):
        # load file
        if self.gv.is_separate:
            # self.sound = self.sw.numpy2AudioSegment(
            #     wav_data, self.gv.SAMPLE_WIDTH, self.gv.RATE, self.gv.CHANNELS)
            print(len(wav_data))
            exit()
            self.sample = AudioSegment(wav_data, self.gv.SAMPLE_WIDTH, self.gv.RATE, self.gv.CHANNELS)
        else:
            self.sound = ul.load_wav(self.path)
            self.sample = self.sound._data

        print(self.sample)
        print(len(self.sample))
        # self.sample = self.sound['data']
        # s = AudioSegment(self.sample, self.gv.SAMPLE_WIDTH, self.gv.RATE, self.gv.CHANNELS)

        # self.sample = np.array(self.sample)
        # print(self.sample)
        # print(type(self.sample))

        # self.sound = ul.load_wav(self.path)
        # print(self.sound._data)

        exit()

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

    def save_datas(self, it):
        fname = self.path.name

        # save image (== figure)
        if self.gv.is_save_img:
            img_exp_dir = self.img_exp_base.joinpath(self.path.parent)
            exp_path = img_exp_dir.joinpath(f'{fname}_{it}.jpg')
            print(exp_path)

            # plt.savefig(exp_path)
            # print(f'Save to {exp_path}')

        # save wav
        #   when file is separated
        if self.gv.is_save_wav and self.gv.is_separate:
            wav_exp_dir = self.wav_exp_base.joinpath(self.path.parent)
            exp_path = wav_exp_dir.joinpath(f'{fname}_{it}.wav')
            print(exp_path)

            # self.sw.write_wav(1, exp_path)
            # print(f'Save to {exp_path}')

        # 切り取るなら
        if self.gv.is_crop:
            ul.crop(self.gv.crop_range)

    def main(self, params):
        # while (it < argv_len):
        for i, wav_file in enumerate(params):
            self.path = Path(wav_file)

            # 存在しないなら continue
            if not self.path.exists():
                # it += 1
                continue

            # fname = self.path.stem
            # ext = self.path.suffix

            # wav ファイルでないなら continue
            if self.path.suffix[1:] != 'wav':
                print('not wav.')
                # it += 1
                continue

            # it = 0
            wav_data = None

            tmp_params = [self.path.__str__(), self.gv.CUT_TIME]
            # while(True):
            for it, wav_data in enumerate(self.sw.cut_wav(*tmp_params)):
                # 変換
                self.conv_and_plot(wav_data)
                self.save_datas(it)

                # it += 1
                # break
