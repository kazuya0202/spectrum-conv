import matplotlib.pyplot as plt
import sys
import os
import numpy as np
from pydub import AudioSegment
from recognize import SoundRecognition
from record import Record
from util import Util

import glob
# import librosa


def numpy2AudioSegment(data):
    """
    dataをnumpy配列からAudioSegmentに変換する
    ARGS:
        data (ndarray): 音データ
    RETURNS:
        sound (AudioSegment): 変換後の音データ
    """

    sound = AudioSegment(
        data=data,
        sample_width=2,
        frame_rate=44100,
        channels=1
    )
    return sound


def append_white_noise(data, noise_ratio=3000):
    """
    ホワイトノイズ付加
    """

    # ノイズ生成
    noise = np.random.randn(len(data))

    # ノイズ付加
    augmented_data = data + noise_ratio * noise
    augmented_data = augmented_data.astype(type(data[0]))

    return augmented_data


if __name__ == '__main__':
    # target wav files
    # glob_path = './wav/pooon/*.wav'

    # export path
    # exp_path = 'augmented_noise'

    argv = sys.argv
    if len(argv) <= 2:
        print('Usage: python augmentation.py <wav_folder> [export_path]')
        print()
        print('  - python augmentation.py ./wav augmented')
        print('  - python augmentation.py ./wav')
        print()
        print('  default export_path: export/')
        exit()

    glob_path = argv[1]
    exp_path = argv[2] if len(argv) >= 3 else 'export'

    glob_path += '/*.wav'

    # if len(argv) >= 2:
    #     glob_path = argv[1]

    # if len(argv) >= 3:
    #     exp_path = argv[2]

    if not os.path.exists(exp_path):
        os.makedirs(exp_path)

    # spec = Spectrum(export_path=exp_path, crop_range=(138, 63, 518, 427))
    sr = SoundRecognition()
    rc = Record()

    noise_range = 5000
    step = 1000
    start = 4000

    img_name = []
    for file in glob.glob(glob_path):
        wav_path = file
        sound = rc.load_wav(wav_path)  # 読み込み
        sample = sound._data

        save_path = os.path.basename(wav_path)
        save_path = os.path.splitext(save_path)[0]

        # ↓違くて草
        # (5000 / 1000) == 5
        #   not    : range(5 + 1) => 6 times.
        #   correct: range(5) == (0 ~ 4) + 1 => (1 ~ 5)
        for i in range((noise_range // step) + 1):
            # ノイズの強さ
            noise_ratio = (i) * step

            if noise_ratio <= start:
                continue

            path = './{}/{}_{}.wav'.format(exp_path, save_path, i)
            print(path)

            augmented_data = append_white_noise(sample, noise_ratio)

            sound = numpy2AudioSegment(augmented_data)
            sr.convert(path, sound, exp_path=exp_path)
