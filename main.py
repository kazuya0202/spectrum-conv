import sys
import matplotlib.pyplot as plt
from pathlib import Path
import numpy as np

# my packages
import utils as ul
from spectrum_conv import SpectrumConversion
from global_variables import GlobalVariables
from separate_wav import SeparateWave
from audio_augment import AudioAugmentation


class Main:
    def __init__(self):
        self.gv = GlobalVariables()

        plt_conf = self.determine_plot_config(self.gv.plt_conf)

        self.sc = SpectrumConversion(plt_conf=plt_conf)
        self.aa = AudioAugmentation()
        self.sw = SeparateWave(None)    # temporary

        # wav ファイルのパス
        self.path = Path('')

        # 出力先のベース
        self.wav_exp_base = Path(self.gv.wav_exp_dir)
        self.img_exp_base = Path(self.gv.img_exp_dir)

        # 出力先のディレクトリ
        self.wav_exp_dir = Path('')
        self.img_exp_dir = Path('')

        # save config
        if not self.gv.is_save_img:
            self.gv.is_save_augmented_img = False
        if not self.gv.is_save_wav:
            self.gv.is_save_augmented_wav = False

    def save_datas(self, plt_fig=None, wav_data=None, exp_path=''):
        """[summary]

        Args:
            plt_fig ([type], optional): [description]. Defaults to None.
            wav_data ([type], optional): [description]. Defaults to None.
            exp_path (str, optional): export file name. Defaults to ''.
        """

        # all save data is None
        if plt_fig is None and wav_data is None:
            return

        exp_path = Path(exp_path)
        print('\nSave to:')

        # --- save img ---
        if plt_fig is not None:
            jpg_name = f'{exp_path}.jpg'
            img_path = self.img_exp_dir.joinpath(jpg_name)

            plt_fig.savefig(str(img_path))
            print(f'  {img_path}')

            # 切り取るなら
            if self.gv.is_crop:
                ul.crop_img(self.gv.crop_range, img_path)
                print(f'    -> croped.')

        # --- save wav ---
        #   when file is separated
        if wav_data is not None:
            wav_name = f'{exp_path}.wav'
            wav_path = self.wav_exp_dir.joinpath(wav_name)

            self.sw.save_as_wav(str(wav_path))
            print(f'  {wav_path}')

        """ MEMO
        毎回挟まないと、cbarが無限に増えていく現象が起こった
        """
        # clear cache
        plt.clf()

    def determine_save_path(self):
        parent = self.path.parent
        stem = self.path.stem

        # if self.gv.is_audio_augment:
        #     if self.gv.is_save_augmented_img \
        #         or self.gv.is_save_augmented_wav:
        #         stem += '-augmented'

        # save path
        self.img_exp_dir = self.img_exp_base.joinpath(parent)
        self.wav_exp_dir = self.wav_exp_base.joinpath(parent)

        # child dir
        if self.gv.is_separate:
            self.img_exp_dir = self.img_exp_dir.joinpath(stem)
            self.wav_exp_dir = self.wav_exp_dir.joinpath(stem)

        # mkdir
        if self.gv.is_save_img:
            self.img_exp_dir.mkdir(parents=True, exist_ok=True)

        if self.gv.is_save_wav:
            self.wav_exp_dir.mkdir(parents=True, exist_ok=True)

    def determine_plot_config(self, conf):
        """ プロットの設定を決定する """
        # conf = self.gv.plt_conf
        plt_conf = {}

        _x, _y = (conf['x'], conf['y']) if conf['xy'] else (False, False)
        _square = True if self.gv.is_separate else conf['square']

        plt_conf['x'] = _x
        plt_conf['y'] = _y
        plt_conf['cbar'] = conf['cbar']
        plt_conf['cmap'] = conf['cmap']
        plt_conf['vmin'] = conf['vmin']
        plt_conf['square'] = _square

        return plt_conf

    def process_argv(self, argv):
        if ul.has_elems_in_list(argv, ['-h', '--help']):
            print('Usage:')
            print('  python <this-file>.py **/*.wav')
            print('  python <this-file>.py <audio_file>.wav')
            print('  python <this-file>.py')
            exit()

        if ul.has_elems_in_list(argv, ['-t', '--test']):
            print('It specified a \'test\' option.')
            print('This feature is unimplemented.')
            exit()

        if len(argv) == 1:
            fpath = input('> Enter file path: ')
            argv.append(fpath)

        # remove <script>.py to ignore
        argv.remove(argv[0])

        return argv

    def convert(self, sound):
        plt_fig = self.sc.conv_and_plot(sound)
        is_show = any([self.gv.plt_show_img, self.gv.plt_show_pause])

        if self.gv.plt_conf['xy'] and is_show:
            # 軸を見やすくする
            self.sc.change_axis_range(
                xtick_interval=self.gv.plt_xtick_interval,
                ytick_interval=self.gv.plt_ytick_interval)

        # 表示するかどうか
        if self.gv.plt_show_img:
            plt.show()

        if self.gv.plt_show_pause:
            plt.pause(self.gv.plt_pause_interval)

        return plt_fig

    def main(self):
        argv = self.process_argv(sys.argv)

        for i, wav_file in enumerate(argv):
            self.path = Path(wav_file)

            # 存在しないなら continue
            if not self.path.exists():
                continue

            # wav ファイルでないなら continue
            if not self.path.suffix == '.wav':
                # ffmpeg つかって encode 関数でも作る?
                print('It is not wav file.')
                continue

            # 保存先を決定
            self.determine_save_path()
            self.sw = SeparateWave(str(self.path), load_wave=True)

            if self.gv.is_separate:
                # 切り分けて処理

                # generator
                params = [self.gv.cut_interval, self.gv.shift_time]
                separated_waves = self.sw.separate_wav(*params)

                for it, wav_data in enumerate(separated_waves):
                    # 切り分けが終了したら break
                    if wav_data is None:
                        break

                    # convert numpy to AudioSegment
                    self.sw.data = wav_data
                    self.sw.numpy2AudioSegment()

                    # conv, plot, save
                    plt_fig = self.convert(self.sw.sound)

                    exp_path = f'{self.path.stem}_{it}'

                    x = plt_fig if self.gv.is_save_img else None
                    y = wav_data if self.gv.is_save_wav else None
                    self.save_datas(x, y, exp_path)

                    # audio augmentation
                    if self.gv.is_audio_augment:
                        self.augment(wav_data, base_exp_path=exp_path)

            else:
                # 引数のファイルをそのまま変換する場合

                self.sw.numpy2AudioSegment()

                # conv, plot, save
                plt_fig = self.convert(self.sw.sound)

                exp_path = f'{self.path.stem}'

                x = plt_fig if self.gv.is_save_img else None
                y = None    # original file -> do not save
                self.save_datas(x, y, exp_path)

                # audio augmentation
                if self.gv.is_audio_augment:
                    self.augment(self.sw.sound._data, base_exp_path=exp_path)

        return 0

    def augment(self, data, base_exp_path):
        """ White Noise """
        if self.gv.aa_exec_whitenoise:
            _max = max(self.gv.whitenoise_range)
            _min = min(self.gv.whitenoise_range)
            step = self.gv.whitenoise_step

            num = ((_max - _min) // step) + 1
            noise_range = np.linspace(_min, _max, num)

            # remove 0
            # 0 noise -> same as original data
            if _min == 0:
                noise_range = noise_range[1:]

            for _, ratio in enumerate(noise_range):
                # append white noise
                params = [data, ratio]
                augmented_data = self.aa.append_white_noise(*params)

                # convert numpy to AudioSegment
                self.sw.data = augmented_data
                self.sw.numpy2AudioSegment()

                # conv, plot, save
                plt_fig = self.convert(self.sw.sound)
                exp_path = f'{base_exp_path}_noise[{int(ratio)}]'

                x = plt_fig if self.gv.is_save_augmented_img else None
                y = augmented_data if self.gv.is_save_augmented_wav else None
                self.save_datas(x, y, exp_path)

        # another augmentation


if __name__ == '__main__':
    m = Main()
    exit_status = m.main()

    sys.exit(exit_status)
