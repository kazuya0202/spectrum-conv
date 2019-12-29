import librosa
from pathlib import Path
import sys
import numpy as np
import matplotlib.pyplot as plt


def change_speed(data, rate):
    return librosa.effects.pitch_shift(data, rate, n_steps=4)


if __name__ == "__main__":
    print('change speed.')

    from separate_wav import SeparateWave

    p = './crossing-sample.wav'
    sw = SeparateWave(p)
    sw.numpy2AudioSegment()
    plt.plot(sw.sound._data)
    plt.pause(1)
    plt.close()

    y, sr = librosa.load(p)
    aug = change_speed(y, sr)
    # aug = change_speed(sw.sound._data, sw.fr)
    plt.plot(aug)
    plt.pause(1)
