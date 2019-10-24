import matplotlib.pyplot as plt
import sys
import os
import numpy as np
from pydub import AudioSegment
# sys.path.append('../../../prcn2019/#realtime-recognition/_test/')
# from spectrum import Spectrum
# from record import Record
from recognize import SoundRecognition
from record import Record

import glob
import librosa


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
    exp_path = 'augmented_noise'
    # spec = Spectrum(export_path=exp_path, crop_range=(138, 63, 518, 427))
    sr = SoundRecognition()
    rc = Record()

    noise_range = 5000
    step = 1000
    start = 4000

    img_name = []
    glob_path = './wav/pooon/*.wav'
    for file in glob.glob(glob_path):
        wav_path = file
        sound = rc.load_wav(wav_path)  # 読み込み
        sample = sound._data

        save_path = os.path.basename(wav_path)
        save_path = os.path.splitext(save_path)[0]

        for i in range((noise_range // step) + 1):
            # ノイズの強さ
            noise_ratio = (i) * step

            if noise_ratio <= start:
                continue

            path = './{}/{}_{}.wav'.format(exp_path, save_path, i)
            print(path)

            augmented_data = append_white_noise(sample, noise_ratio)

            sound = numpy2AudioSegment(augmented_data)
            sr.convert(path, sound)
