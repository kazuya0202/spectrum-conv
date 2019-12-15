import matplotlib.pyplot as plt


class GlobalVariables:
    def __init__(self):
        # =============== USER_SETTINGS =================

        # 保存するかどうか
        self.is_save_img = True   # 画像
        self.is_save_wav = False   # 切り分けた wav
        # is_save_wav は is_separate == True のときのみ判別する
        # => separate しないのに保存はしない

        # wav を1秒ごとに切り分けるかどうか
        self.is_separate = True

        # 切り取るかどうか
        self.is_crop = True

        # データセット作成用かどうか (unimplemented)
        # => xy, cbar        : False
        # => self.is_save_img: True
        # => self.is_separate: True
        # => self.is_crop    : True
        # => self.is_augment : True (?)
        self.is_learning_data = False

        # 増幅するかどうか (unimplemented)
        self.is_audio_augment = True

        # librosa 使えるならもっと？
        self.aa_exec_whitenoise = False
        self.aa_exec_change_pitch = False
        self.aa_exec_change_speed = False

        """ MEMO
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

        # 増幅したデータを保存するかどうか
        self.is_save_augmented_img = False
        self.is_save_augmented_wav = False

        # plot config
        self.plt_conf = {
            # X, Y 軸を表示するかどうか
            'xy': False,

            # カラーバーを表示するかどうか
            'cbar': False,

            # ===== 特に変更する必要はない =====
            # X, Y 軸の目盛り間隔
            'x': 1,
            'y': 1,

            # プロットカラー
            'cmap': plt.cm.gist_rainbow_r,

            # 画像の色を調節
            'vmin': -1,

            # 正方形(?)でプロットするかどうか
            # => self.is_separate == True なら自動的に True
            'square': True
        }

        # ===== 確認用（debug）==========================
        # プロットした画像をウィンドウで表示するかどうか
        # => ウィンドウを閉じるまで処理は進まない
        self.plt_show_img = False

        # 順番にウィンドウで表示するかどうか
        # => N秒ごとに更新
        self.plt_show_pause = False
        self.plt_pause_interval = 0.2

        # ----- 特に変更する必要はない ------------------
        # X 軸の tick 間隔（N回に1回表示）
        self.plt_xtick_interval = 10

        # Y 軸の tick 間隔（N回に1回表示）
        self.plt_ytick_interval = 4
        # ===============================================

        # ============== COMPLEX_SETTINGS ===============
        """ SPECTRUM_CONVERTION """
        # 画像出力先ディレクトリ
        self.img_exp_dir = 'spectrum-img'

        # wav 出力先ディレクトリ
        self.wav_exp_dir = 'wav_exp'

        # 画像の切り取り範囲
        # (Y_top, X_left, Y_bottom, X_right)
        self.crop_range = (143, 58, 514, 427)
        """ MEMO
        branch crop_range by option
            - all([conf['cbar'], conf['xy']])
            - conf['cbar']
            - conf['xy']
            - None (inplemented)
        """

        """ AUGMENTATION """
        # 1000 ~ 4000
        self.whitenoise_range = [1000, 4000]
        # step by 1000
        self.augment_step = 1000

        """ SEPARATE_WAVE """
        self.shift_time = 0.1
        self.cut_interval = 1.05

        # when SeparateWave's member variables is 0
        self.width = 2
        self.fr = 44100
        self.ch = 2
        self.ch = 1
