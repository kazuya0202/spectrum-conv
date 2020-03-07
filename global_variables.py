import matplotlib.pyplot as plt


class GlobalVariables:
    def __init__(self):
        # =============== USER_SETTINGS =================

        self.is_separate = True  # wav を1秒ごとに切り分けるかどうか
        self.resize_size = (300, 300)  # (height, width)

        # 保存するかどうか
        self.is_save_img = True  # 画像
        self.is_save_wav = False  # 切り分けた wav

        # 増幅するかどうか (white noise)
        self.is_audio_augment = True
        # separate == False, のときうまくプロットされない

        """ AUDIO AUGMENTATION """
        self.whitenoise_percentage = [5, 15]  # n % ~ m %
        self.whitenoise_step = 5  # 段階(刻み)

        """ SEPARATE WAVE """
        self.shift_time = 0.2  # ずらす間隔
        self.cut_interval = 1  # 切り取り間隔

        #  vflip |   True   |  False
        # -------+----------+----------
        #  上部  | 高周波数 | 低周波数
        # [画像] |    ↕    |    ↕
        #  下部  | 低周波数 | 高周波数
        self.vflip = True  # 垂直反転

        # plot config
        self.plt_conf = {
            "xy": False,  # X, Y 軸を表示するかどうか
            "cbar": False,  # カラーバーを表示するかどうか
            # ===== 特に変更する必要はない =====
            "x": 1,  # X, Y 軸の目盛り間隔
            "y": 1,
            "cmap": plt.cm.gist_rainbow_r,  # プロットカラー
            "vmin": -1,  # 画像の色を調節
            "square": True,  # 正方形(?)でプロットするかどうか
            # => self.is_separate == True なら自動的に True
        }

        # ----- 確認用（debug）---------------------------
        # プロットした画像をウィンドウで表示するかどうか
        # => ウィンドウを閉じるまで処理は進まない
        self.plt_show_img = False

        # 順番にウィンドウで表示するかどうか
        # => N秒ごとに更新
        self.plt_show_pause = True
        self.plt_pause_interval = 0.01

        # ============== COMPLEX_SETTINGS ===============

        """ MAIN """
        self.img_exp_dir = "spectrum-img"  # 画像出力先ディレクトリ
        self.wav_exp_dir = "wav_exp"  # wav 出力先ディレクトリ

        # 増幅の種類 (librosa 使えるならもっと?)
        self.aa_exec_whitenoise = True  # implemented
        # self.aa_exec_change_pitch = False  # unimplemented
        # self.aa_exec_change_speed = False  # unimplemented

        # ----- plot config (特に変更する必要はない)---
        # X 軸の tick 間隔（N回に1回表示）
        self.plt_xtick_interval = 10

        # Y 軸の tick 間隔（N回に1回表示）
        self.plt_ytick_interval = 4

        # ==========================================
        """ MEMO - crop
        branch crop_range by option
            - all([conf['cbar'], conf['xy']])
            - conf['cbar']
            - conf['xy']
            - None (inplemented)
        """

        """ MEMO - augmentation
        augment list:
            whtienoise (noise)
                - valid
                - already implemented
            shift
                - valid
                - already implemented (same as cut_wav)
            speed
                - valid
                - unimplemented
            stretch (?= pitch)
                - valid
                - case of env sound is invalid ?
        """

        # データセット作成用かどうか (unimplemented)
        # => xy, cbar        : False
        # => self.is_save_img: True
        # => self.is_separate: True
        # => self.is_crop    : True
        # => self.is_augment : True (?)
        self.is_learning_data = False
