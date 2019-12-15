import wave
import numpy as np
from scipy import int16, frombuffer


class SeparateWave:
    def __init__(self):
        self.ch = 0
        self.width = 0
        self.fr = 0
        self.fn = 0

    def cut_wav(self, path, cut_interval, shift_time):
        data = None
        with wave.open(path, 'r') as w:
            self.ch = w.getnchannels()
            self.width = w.getsampwidth()
            self.fr = w.getframerate()
            self.fn = w.getnframes()
            data = w.readframes(w.getnframes())

        total_time = 1.0 * self.fn / self.fr
        total_time_int = np.floor(total_time)
        st = shift_time
        # st = int(shift_time)

        # フレームに応じて図の横幅が変わるため、一定値にする
        frames = int(self.ch * self.fr * st)

        num_cut = int(total_time_int // st)

        # -- for debug
        # print(f'channle: {self.ch}')
        # print(f'sample width: {self.width}')
        # print(f'frame rate: {self.fr}')
        # print(f'frame num: {self.fn}')
        # # print(f'params: {wr.getparams()}')
        # print(f'total time: {total_time}')
        # print(f'total time(int): {total_time_int}')
        # print(f'cut time: {st}')
        # print(f'frames: {frames}')
        # print(f'number of cut: {num_cut}')

        sample = frombuffer(data, dtype=int16)
        end_condition = frames * num_cut

        # 実際の frames と変更するため注意
        # => end_condition で配列外参照を防ぐ
        frames = 10000  # 横幅を合わせるため
        interval = cut_interval * 10

        for i in range(num_cut):
            # print(i)

            bgn = int(i * frames)
            end = int((i + interval) * frames)
            # end = (i + 11) * frames
            """
                (i + 10) => 1 sec.

                画像的に真四角にならないから
                (i + 11) => 1 + N sec.
            """

            # frame を超えたら None
            if end >= end_condition:
                # print('  over frames')
                return None

            wav_data = sample[bgn:end]

            # generator
            yield wav_data
