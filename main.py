import sys
import matplotlib.pyplot as plt
from pathlib import Path
import numpy as np

import utils as ul
from spectrum_conv import SpectrumConversion
from global_variables import GlobalVariables
from separate_wav import SeparateWave
from audio_augment import AudioAugmentation


class Main:
    def __init__(self):
        self.gv = GlobalVariables()

        plt_conf = self.determine_plot_config()

        self.sc = SpectrumConversion(plt_conf=plt_conf)
        self.sw = SeparateWave()
        self.aa = AudioAugmentation()

        # wav ファイルのパス
        self.path = Path('')

        # 出力先のベース
        self.wav_exp_base = Path(self.gv.wav_exp_dir)
        self.img_exp_base = Path(self.gv.img_exp_dir)

        # 出力先のディレクトリ
        self.wav_exp_dir = Path('')
        self.img_exp_dir = Path('')

        # プロットされた図のデータ
        self.plt_fig = None

    def save_datas(self, plt_fig=None, wav_data=None, exp_path=''):
        """[summary]

        Args:
            plt_fig ([type], optional): [description]. Defaults to None.
            wav_data ([type], optional): [description]. Defaults to None.
            exp_path (str, optional): ファイル名の末尾に追加する文字列（連番）. Defaults to ''.
        """

        # 拡張子の切り分け
        exp_path = str(Path(exp_path).stem)

        if self.gv.is_save_img or self.gv.is_save_wav:
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
        if self.gv.is_separate and self.gv.is_save_wav:
            if wav_data is not None:

                wav_name = f'{exp_path}.wav'
                wav_path = self.wav_exp_dir.joinpath(wav_name)

                # separate するときに読み込んだ元のデータの値で書き出す
                params = [wav_data, self.sw.width,
                          self.sw.fr, self.sw.ch, str(wav_path)]
                ul.save_as_wav(*params)
                print(f'  {wav_path}')

        """ MEMO
        なんか毎回挟まないと、cbarが無限に増えていく現象が起こった
        """
        # clear cache
        plt.clf()

    def determine_save_path(self):
        parent = self.path.parent
        stem = self.path.stem

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

    def determine_plot_config(self):
        """ プロットの設定を決定する """
        conf = self.gv.plt_conf
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

    def main(self):
        argv = self.process_argv(sys.argv)

        for i, wav_file in enumerate(argv):
            self.path = Path(wav_file)

            # 存在しないなら continue
            if not self.path.exists():
                continue

            # wav ファイルでないなら continue
            if not self.path.suffix[1:] == 'wav':
                # ffmpeg つかって encode 関数でも作る?
                print('not wav file.')
                continue

            # 保存先を決定
            self.determine_save_path()

            if self.gv.is_separate:
                # 切り分けて処理

                # generator
                params = [str(self.path), self.gv.cut_interval,
                          self.gv.shift_time]
                separated_waves = self.sw.cut_wav(*params)

                for it, wav_data in enumerate(separated_waves):
                    # 切り分けが終了したら break
                    if wav_data is None:
                        break

                    # convert numpy to AudioSegment
                    params = [wav_data, self.sw.width, self.sw.fr, self.sw.ch]
                    sound = ul.numpy2AudioSegment(*params)

                    # conv, plot, save
                    plt_fig = self.sc.conv_and_plot(sound)

                    # append_str = f'_{it}'
                    exp_path = f'{self.path.stem}_{it}'
                    _ = self.save_datas(plt_fig, wav_data, exp_path)
            else:
                # 引数のファイルをそのまま変換する場合

                # load file
                sound = ul.load_wav(str(self.path))

                # conv, plot, save
                plt_fig = self.sc.conv_and_plot(sound)

                exp_path = f'{self.path.stem}'
                _ = self.save_datas(plt_fig=plt_fig, exp_path=exp_path)
                # continue

            # clear cache
            # plt.clf()

        return 0

    def ab(self, it=None):
        if self.gv.is_audio_augment:
            _max = max(self.gv.whitenoise_range)
            _min = min(self.gv.whitenoise_range)
            step = self.gv.augment_step

            num = ((_max - _min) // step) + 1
            noise_range = np.linspace(_min, _max, num)[1:]

            # append_str_base = f'_{it}'

            """ White Noise """
            for i, ratio in enumerate(noise_range):
                print(ratio)
                # continue

                wav_data = None

                # append white noise
                params = [wav_data, ratio]
                augmented_data = self.aa.append_white_noise(*params)

                # convert numpy to AudioSegment
                params = [augmented_data, self.sw.width, self.sw.fr, self.sw.ch]
                sound = ul.numpy2AudioSegment(*params)

                # conv, plot, save
                plt_fig = self.sc.conv_and_plot(sound)

                exp_path = f'{self.path.stem}_it_noise{i}'
                _ = self.save_datas(plt_fig, augmented_data, exp_path)

            # change speed, stretch (?= change pitch)
            """  """

            print('augmented.')


if __name__ == '__main__':
    # Main().ab()
    # exit()

    m = Main()
    exit_status = m.main()

    sys.exit(exit_status)
