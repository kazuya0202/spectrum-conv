import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


class SpectrumConversion:
    def __init__(self, plt_conf=None):
        # プロットの設定
        self.plt_conf = {
            'x': False,
            'y': False,
            'cbar': False,
            'cmap': plt.cm.gist_rainbow_r,
            'vmin': -1,
            'square': True
        }

        if plt_conf is not None:
            self.plt_conf = plt_conf

    def conv_and_plot(self, sound):
        sample = sound._data

        """ スペクトログラム作成 """
        w = 1024  # 窓枠
        s = 512   # 刻み

        ampList = []  # スペクトル格納用
        argList = []  # 偏角格納用

        i = None
        data = None

        # 刻みずつずらしながら窓幅分のデータをフーリエ変換
        print(((sample.shape[0] - w) / s))
        for i in range(int((sample.shape[0] - w) / s)):
            data = sample[i * s:i * s + w]
            spec = np.fft.fft(data)
            spec = spec[:int(spec.shape[0] / 2)]
            spec[0] /= 2
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

        # seaborn の heatmap を使う
        plt_data = pd.DataFrame(data=ampList, index=time, columns=freq)

        # plot config
        xticklabels = self.plt_conf['x']
        yticklabels = self.plt_conf['y']
        cmap = self.plt_conf['cmap']
        vmin = self.plt_conf['vmin']
        cbar = self.plt_conf['cbar']
        square = self.plt_conf['square']

        sns.heatmap(data=np.log(plt_data.iloc[:, :100].T),
                    xticklabels=xticklabels,
                    yticklabels=yticklabels,
                    cmap=cmap,
                    vmin=vmin,
                    cbar=cbar,
                    square=square)

        # Y軸の反転
        ax = plt.gca()
        ax.invert_yaxis()

        # プロットした図を保存
        plt_fig = plt.gcf()

        return plt_fig

        # ax.set_xticklabels(xs)
        # ax.set_yticklabels(ys)
        # ax.set_xticklabels('{}'.format(str(x)) for x in xs)
        # ax.set_yticklabels(['{:,.2%}'.format(x) for x in ])

        # for v in vals:
        # import matplotlib.ticker as ticker
        # ax.get_xaxis().get_major_formatter().set_useOffset(False)
        # ax.get_xaxis().set_major_locator(ticker.MaxNLocator(integer=True))

        # xs = [x.get_text() for x in plt.xticks()[1]]
        # ys = [y.get_text() for y in plt.yticks()[1]]

        # print(xs)

        # xs = [(float(x)) for x in xs]
        # ys = [(float(y)) for y in ys]

        # xxs = np.linspace(min(xs), max(xs), 11)
        # yys = np.linspace(min(ys), max(ys), 11)

        # xticks = plt.xticks()
        # print(type(xticks[0]))
        # print(type(xticks[1]))
        # # print(xticks[1])
        # for x in xticks[1]:
        #     print(x)

        # ax.xaxis.set_ticks(xxs)
        # ax.yaxis.set_ticks(yys)
        # ax.xaxis.set_ticks(['{:.2f}'.format(x) for x in xxs])
        # ax.yaxis.set_ticks(['{:.2f}'.format(x) for x in yys])
        # plt.xticks(np.arange(min(xxs), max(xxs), 10))
        # plt.yticks(np.arange(min(yys), max(yys), 10))
        # plt.ylim(min(yys), max(yys))
        # plt.xlim(min(xxs), max(xxs))

        # ticks0 = []
        # # ticks1 = []
        # ticks1 = plt.cbook.silent_list()
        # for i, x in enumerate(xxs):
        #     p = i * 10
        #     ticks0.append(p)
        #     ticks1.append(plt.Text(p, 0, x))

        # ticks0 = np.array(ticks0)
        # print(type(ticks1))
        # # for a in ticks1:
        # #     print(a)
        # plt.xticks([ticks0, ticks1])
        # plt.yticks(yys)

        # plt.xticks(np.arange(len(xxs)), xxs)
        # plt.yticks(np.arange(len(yys)), yys)
        # ax.set(xticks=xxs, yticks=yys)

        # from matplotlib import ticker
        # ax.xaxis.set_major_formatter(ticker.FormatStrFormatter('%0.1f'))
        # ax.yaxis.set_major_formatter(ticker.FormatStrFormatter('%0.1f'))

        # ticks = 10
        # plt.xticks(range(0, len(plt_data), ticks), plt_data[::ticks])

    def change_axis_range(self, xtick_interval=1, ytick_interval=1):
        """ MEMO
        時間軸（X）はファイルが長いのに対応できてないから
        調整いるかも
        """

        # 軸の目盛りを調整する
        def fill_label(labels, interval):
            """ 表示間隔を変更 """
            for i, label in enumerate(labels):
                if (i % interval == 0) or ((len(labels) - 1) == i):
                    txt = label.get_text()
                    labels[i] = txt[:txt.find('.') + 3]
                else:
                    labels[i] = ''
            return labels

        # 各軸のラベルを取得
        x_labels = plt.xticks()[1]
        y_labels = plt.yticks()[1]

        X = fill_label(x_labels, xtick_interval)
        Y = fill_label(y_labels, ytick_interval)

        # 変更したラベルを設定
        plt.xticks(ticks=np.arange(len(X)), labels=X, rotation=90)
        plt.yticks(ticks=np.arange(len(Y)), labels=Y)
