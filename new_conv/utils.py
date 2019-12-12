import os
from pydub import AudioSegment
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path


class Utils:
    def __init__(self):
        pass

    def has_elems_in_list(self, _list, elems):
        if type(_list) == list or type(_list) == tuple:
            res = [True if elem in _list else False for elem in elems]
            return any(res)

        return elems in _list

    # OS
    def make_dirs(self, dir_name):
        """指定したディレクトリが存在しなければディレクトリを作成"""
        if not Path.exists(dir_name):
            os.makedirs(dir_name)

    def splitext(self, path):
        """拡張子で区切る"""
        sp = os.path.splitext(path)
        return (sp[0], sp[1])

    def get_fname(self, path):
        """ファイル名のみを取得"""
        fname = self.splitext(path)[0]
        return fname

    def get_ext(self, path):
        """拡張子のみを取得"""
        ext = self.splitext(path)[1][1:]
        return ext

    # SPECTRUM
    def load_wav(self, wav_path):
        """wavファイルを読み込む"""
        # 読み込み
        sound = AudioSegment.from_wav(wav_path)

        # サンプルデータ取得
        samples = np.array(sound.get_array_of_samples())
        sample = samples[::sound.channels]
        sound._data = sample

        return sound

    def crop(self, crop_range):
        print(f'crop_range: {crop_range}')
