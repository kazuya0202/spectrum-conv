import os
from chainer import cuda
import numpy as np

is_debug = True   # for debug


class Util():
    """ 共通設定 """

    def __init__(self):

        # ----- Detect Frequency ---------------
        # しきい値
        self.threshold = (9000000, 2500000)

        # しきい値を認識する範囲（誤差）
        self.err_range = (3, 5)

        # 各データと対応するラベル
        self.data = [
            # [freq], label
            ([700, 43400], 0),   # crossing
            ([748, 43352], 0),   # crossing
            ([772, 43328], 0),   # crossing
            ([1198, 42902], 0),  # crossing
            ([1351, 42749], 0),  # crossing
            ([1498, 42602], 0),  # crossing

            ([960, 43140], 1),   # klaxon
            ([975, 43125], 1),   # klaxon
            ([988, 43112], 1),   # klaxon
            ([996, 43104], 1),   # klaxon
            ([1013, 43087], 1),  # klaxon
            ([1238, 42862], 1),  # klaxon
        ]

        # ----- CNN Network ---------------
        # GPUを使用するかどうか
        self.is_use_gpu = True

        # GPUを使用するならcuda, しないならnumpy
        self.env = cuda.cupy if self.is_use_gpu else np

        # ----- Recognize ---------------
        # モデルのパス
        # self.model_path = './models/trained_model.pkl'
        self.model_path = 'C:/ichiya/prcn2019/_SoundRecognition/epoch/9epoch_ymd20190924_hms134549.pkl'

        # 認識対象
        self.labels = {
            # データ : ラベル
            'Crossing': 0,
            'Klaxon': 1,
            'Noise': 2
        }

        # 録音ファイル
        self.wav_path = 'file.wav'

        # 画像の切り取りをするかどうか
        self.is_crop = True

        # 画像の切り取り範囲
        self.crop_range = (169, 58, 487, 427)

        # 学習済みモデルへの入力時の画像サイズ
        self.img_width = 60
        self.img_height = 60

        # ----- Record ---------------
        # ファイルの出力先
        self.export_path = 'export'

        # ファイルを保存するかどうか
        self.is_save_file = False

    def make_dir(self, path):
        """ 渡されたパスのディレクトリがない場合は作成する

        Parameters
        ----------
        path: str
            作成したいディレクトリのパス
        """

        if not os.path.exists(path):
            os.makedirs(path)
