class GlobalVariables:
    def __init__(self):
        # conv()
        # 画像出力先ディレクトリ
        self.export_dir = 'spectrum-img'

        # crop()
        # 画像の切り取り範囲
        self.crop_range = (169, 58, 487, 427)

        # 切り取るかどうか
        self.is_crop = True

        # 保存するかどうか
        self.is_save = False

        self.wav_export = 'wav_export'
        self.is_wav_save = False

        # augmentation()
        # 増幅するかどうか
        self.is_augment = False
