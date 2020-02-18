class GlobalVariables:
    def __init__(self):
        import matplotlib.pyplot as plt

        # =============== USER_SETTINGS =================

        self.is_separate = True     # wav を1秒ごとに切り分けるかどうか
        self.is_resize = True  # 画像サイズをリサイズするかどうか
        self.resize_size = (400, 400)

        # 保存するかどうか
        self.is_save_img = True   # 画像
        self.is_save_wav = False   # 切り分けた wav

        # 増幅したデータを保存するかどうか
        # （↑が False なら True でも保存しない）
        # self.is_save_augmented_img = True
        # self.is_save_augmented_wav = False

        # plot config
        self.plt_conf = {
            'xy': False,    # X, Y 軸を表示するかどうか
            'cbar': False,  # カラーバーを表示するかどうか

            # ===== 特に変更する必要はない =====
            'x': 1,     # X, Y 軸の目盛り間隔
            'y': 1,
            'cmap': plt.cm.gist_rainbow_r,  # プロットカラー
            'vmin': -1,     # 画像の色を調節

            # => self.is_separate == True なら自動的に True
            'square': True  # 正方形(?)でプロットするかどうか
        }

        # 増幅するかどうか
        self.is_audio_augment = True
        # separate == False, のときうまくプロットされない

        # 増幅の種類 (librosa 使えるならもっと?)
        self.aa_exec_whitenoise = True      # implemented
        # self.aa_exec_change_pitch = False  # unimplemented
        # self.aa_exec_change_speed = False  # unimplemented

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
        self.img_exp_dir = 'spectrum-img'   # 画像出力先ディレクトリ
        self.wav_exp_dir = 'wav_exp'        # wav 出力先ディレクトリ

        """ AUDIO AUGMENTATION """
        self.whitenoise_percentage = [5, 15]  # n % ~ m %
        self.whitenoise_step = 5      # 段階(刻み)

        """ SEPARATE WAVE """
        # ずらす間隔
        self.shift_time = 0.5
        self.cut_interval = 1.05

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
