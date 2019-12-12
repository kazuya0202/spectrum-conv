import wave
import struct
import numpy as np
import os
import sys
from scipy import int16, frombuffer
from pydub import AudioSegment


class SeparateWav:
    def __init__(self):
        pass

    def cut_wav(self, path, time, export_dir):
        wav_file = f'{path}.wav'
        wr = wave.open(wav_file, 'r')

        self.ch = wr.getnchannels()
        self.width = wr.getsampwidth()
        self.fr = wr.getframerate()
        self.fn = wr.getnframes()
        total_time = 1.0 * self.fn / self.fr
        integer = np.floor(total_time)
        # t = int(time)
        t = time

        # フレームに応じて図の横幅が変わるため、一定値にする
        frames = int(self.ch * self.fr * t)

        num_cut = int(integer // t)

        print(f'channle: {self.ch}')
        print(f'sample width: {self.width}')
        print(f'frame rate: {self.fr}')
        print(f'frame num: {self.fn}')
        print(f'params: {wr.getparams()}')
        print(f'total time: {total_time}')
        print(f'total time(int): {integer}')
        print(f'time: {t}')
        print(f'frames: {frames}')
        print(f'number of cut: {num_cut}')

        data = wr.readframes(wr.getnframes())
        wr.close()
        X = frombuffer(data, dtype=int16)

        out_file_path = f'{export_dir}/{path}'
        if not os.path.exists(out_file_path):
            os.makedirs(out_file_path)

        end_condition = frames * num_cut

        path = os.path.basename(path)

        frames = 10000  # 横幅を合わせるための
        for i in range(num_cut):
            print(i)

            self.out_file = f'{out_file_path}/{path}_{i}.wav'
            start_cut = i * frames
            end_cut = (i + 10) * frames + frames

            if end_cut > end_condition:
                print('  over frames')
                # return
                yield None

            Y = X[start_cut:end_cut]
            self.wav_data = struct.pack('h' * len(Y), *Y)

            yield self.wav_data

            # output
            # with wave.open(out_file, 'w') as ww:
            #     ww.setnchannels(self.ch)
            #     ww.setsampwidth(self.width)
            #     ww.setframerate(self.fr)
            #     ww.writeframes(out_data)

    def write_wav(self, wav_data, exp_path):
        with wave.open(exp_path, 'w') as ww:
            ww.setnchannels(self.ch)
            ww.setsampwidth(self.width)
            ww.setframerate(self.fr)
            ww.writeframes(wav_data)

    def numpy2AudioSegment(self, data, sample_width, frame_rate, channels):
        """ dataをnumpy配列からAudioSegmentに変換する

        Parameters
        ----------
        data : numpy.ndarray
            音データ

        Returns
        -------
        sound : pydub.audio_segment.AudioSegment
            変換後の音データ
        """

        sound = AudioSegment(
            data=data,
            sample_width=sample_width,
            frame_rate=frame_rate,
            channels=channels)

        return sound
