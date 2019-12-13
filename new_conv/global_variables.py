class GlobalVariables:
    def __init__(self):
        # conv()

        # 画像出力先ディレクトリ
        self.img_exp_dir = 'spectrum-img'
        # wav 出力先ディレクトリ
        self.wav_exp_dir = 'wav_exp'

        # true / false
        self.is_crop = True         # 切り取るかどうか
        self.is_save_img = True     # 画像を保存するかどうか
        self.is_separate = True    # 分離するかどうか
        self.is_save_wav = False    # wav を保存するかどうか
        self.is_augment = False     # 増幅するかどうか

        # is_save_wav は is_separate == True のときのみ判別する
        # => separate しないのに保存はしない

        # crop()
        # 画像の切り取り範囲
        self.crop_range = (169, 58, 487, 427)

        # separate_wav
        self.SAMPLE_WIDTH = 2
        self.RATE = 44100
        self.CHANNELS = 1

        self.CUT_TIME = 1
