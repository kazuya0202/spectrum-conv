from chainer import cuda, Variable, serializers
import chainer.functions as F
import chainer.links as L
import pickle
import os
from PIL import Image
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib as mpl
from util import Util

from util import is_debug   # for debug
mpl.use('Agg')


class SoundRecognition:
    """ 音認識を行う """

    # コンストラクタ
    def __init__(self, model_path=None):
        """
        Parameters
        ----------
        model_path : str, optional
            学習済みモデルのパス, by default None
        """

        # 共通設定
        util = Util()

        # モデルのパスを決定
        if model_path is None:
            model_path = util.model_path

        # 学習済みモデルを読み込む
        # with open(model_path, 'rb') as f:   # pickle
        #     self.model = pickle.load(f)

        # gpu
        # if util.is_use_gpu:
        #     self.model.to_gpu()

        self.labels = util.labels   # ラベル
        self.env = util.env     # cuda / numpy

        self.is_crop = util.is_crop  # 画像を切り取るかどうか
        self.crop_range = util.crop_range   # 切り取り範囲

        self.wav_path = util.wav_path   # wavファイルのパス
        self.export_img_path = util.export_path  # 出力先フォルダ
        self.save_img_path = ''     # 保存先のパス（出力先+ファイル名）

        # 学習済みモデルへの入力時の画像サイズ
        self.width = util.img_width
        self.height = util.img_height

        # 出力先のフォルダ作成
        util.make_dir(self.export_img_path)

    def recognize(self, img_path):
        """ スペクトログラムをモデルに入力して認識する

        Parameters
        ----------
        img_path : str
            画像パス

        Returns
        -------
        ans : int
            予想ラベル
        percentage : float
            一致率
        """

        # 画像を読み込む
        img = Image.open(img_path)
        img = img.resize((self.width, self.height))
        img = self.env.array(img, dtype=self.env.float32)
        img = img[:, :, :3]
        img = img.transpose(2, 0, 1)

        # 学習済みモデルに入力する
        xt = Variable(self.env.array([img], dtype=self.env.float32))
        ydict = self.model(xt)
        y = ydict['fc8']
        y = F.softmax(y.data)

        ans = int(self.env.argmax(y.data))  # 予想
        percentage = max(y.data[0])  # 一致率

        if is_debug:
            print('max:', percentage)

        # 予想ラベルと一致率を返す
        return ans, percentage

    def convert(self, wav_path=None, sound=None, exp_path=None):
        """ 音データをスペクトログラムに変換する

        Parameters
        ----------
        wav_path : str, optional
            wavファイルのパス, by default None
        sound : pydub.audio_segment.AudioSegment, optional
            音データ, by default None

        Returns
        -------
        self.save_img_path : str
            スペクトログラムの保存先のパス
        """
        from record import Record

        # パスの決定
        if wav_path is None:
            wav_path = self.wav_path

        if exp_path is not None:
            self.export_img_path = exp_path

        # ファイル名の取得
        name = os.path.splitext(wav_path)[0]
        name = os.path.basename(name)

        if sound is None:
            sound = Record().load_wav(wav_path)
        sample = sound._data

        # スペクトログラム作成
        w = 1000    # 窓幅
        s = 500     # 刻み

        ampList = []  # スペクトル格納用
        argList = []  # 偏角格納用

        i = None
        data = None

        # 刻みずつずらしながら窓幅分のデータをフーリエ変換
        for i in range(int((sample.shape[0] - w) / s)):
            data = sample[i * s:i * s + w]
            spec = np.fft.fft(data)
            spec = spec[:int(spec.shape[0] / 2)]
            spec[0] = spec[0] / 2
            ampList.append(np.abs(spec))
            argList.append(np.angle(spec))

        # 周期数
        freq = np.fft.fftfreq(data.shape[0], 1.0 / sound.frame_rate)
        freq = freq[:int(freq.shape[0] / 2)]

        # 時間
        time = np.arange(0, i + 1, 1) * s / sound.frame_rate

        # numpyの配列にする
        ampList = np.array(ampList)
        argList = np.array(argList)

        # スペクトログラムをプロット
        plot_data = pd.DataFrame(data=ampList, index=time, columns=freq)
        sns.heatmap(data=np.log(plot_data.iloc[:, :100].T),
                    xticklabels=False,
                    yticklabels=False,
                    cbar=False,
                    cmap=plt.cm.gist_rainbow_r,
                    vmin=1,
                    square=True)

        # 保存
        self.save_img_path = f'{self.export_img_path}/{name}.jpg'
        plt.savefig(self.save_img_path)
        plt.close()

        # 画像を指定範囲に切り取る
        if self.is_crop:
            self.crop()

        return self.save_img_path

    def crop(self):
        """ 画像を切り取る """

        img = Image.open(self.save_img_path)  # 保存
        img_crop = img.crop(self.crop_range)  # 切り取り
        img_crop.save(self.save_img_path)  # 保存
