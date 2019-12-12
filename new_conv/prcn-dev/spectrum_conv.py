from pydub import AudioSegment
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

import os
import sys
import glob

target_dir = 'spectrum-save-img'


def conv(path):
    ext = os.path.splitext(path)[1]

    # read file
    sound = AudioSegment.from_file(path, ext)

    # parameters
    # print(f'channels   = {sound.channels}')
    # print(f'frame_rate = {sound.frame_rate}')
    # print(f'duration   = {sound.duration_seconds}')

    # sample
    samples = np.array(sound.get_array_of_samples())
    sample = samples[::sound.channels]

    """ スペクトログラム作成 """
    w = 1000  # 窓枠
    s = 500  # 刻み

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

    # 周期数は共通なので1回だけ計算（縦軸表示に使う）
    freq = np.fft.fftfreq(data.shape[0], 1.0 / sound.frame_rate)
    freq = freq[:int(freq.shape[0] / 2)]

    # 時間も共通なので1回だけ計算（横軸表示に使う）
    time = np.arange(0, i + 1, 1) * s / sound.frame_rate

    # numpyの配列にする
    ampList = np.array(ampList)
    argList = np.array(argList)

    """ matplotlib と seaborn でスペクトログラムを可視化 """
    df_amp = pd.DataFrame(data=ampList, index=time, columns=freq)

    # プロットサイズ変更
    # plt.figure(figsize=(20, 6))

    # seaborn の heatmap を使う
    plot_data = pd.DataFrame(data=ampList, index=time, columns=freq)
    sns.heatmap(data=np.log(plot_data.iloc[:, :100].T),
                xticklabels=False,
                yticklabels=False,
                cbar=False,
                cmap=plt.cm.gist_rainbow_r,
                vmin=1,
                square=True)

    # save

    # 1階層上のフォルダ名を取得
    p = os.path.dirname(path)
    parent_dir = p[p.rfind('/') + 1:]

    save_path = f'{target_dir}/{parent_dir}'
    if not os.path.exists(save_path):
        os.makedirs(save_path)

    # ファイル名のみを取得
    fname = os.path.basename(path)
    fname = fname[:fname.rfind('.')]

    save_name = f'{save_path}/{fname}.jpg'
    plt.savefig(save_name)
    print(f"Save to '{save_name}'")

    plt.close()

    """ 画像を切り取る """
    from PIL import Image
    # crop_range = (169, 58, 487, 427)
    crop_range = (138, 63, 518, 427)

    img = Image.open(save_name)  # 保存
    img_crop = img.crop(crop_range)  # 切り取り
    img_crop.save(save_name)  # 保存


def main(path=None):
    default = 'crossing1.wav'
    argv = sys.argv

    if path is None:
        path = default

        # 引数があるなら
        if len(argv) >= 2:
            path = argv[1]

    # ファイルなら
    if os.path.isfile(path):
        conv(path)

    # ディレクトリ
    else:
        for file_path in glob.glob(f'{path}/*'):
            # ディレクトリの中にディレクトリがあるなら
            if os.path.isdir(file_path):
                for file in glob.glob(f'{file_path}/*'):
                    conv(file)
            # conv(f'{root}/{f}')
            conv(file_path)


if __name__ == '__main__':
    main()
