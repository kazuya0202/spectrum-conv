import wave
import numpy as np
from scipy import int16, frombuffer
from pydub import AudioSegment


class SeparateWave:
    def __init__(
            self,
            data,
            ch=1,
            width=2,
            fr=44100,
            fn=None,
            load_wave=True,
            is_audio_segment=False):

        # exception
        if data is None:
            return

        if load_wave:
            self.load_wav(data, is_audio_segment)
        else:
            self.data = data
            self.ch = ch
            self.width = width
            self.fr = fr
            self.fn = fn

        self.total_time = 1.0 * self.fn / self.fr
        self.total_time_int = int(np.floor(self.total_time))

        self.sound = None

    def load_wav(self, path, is_audio_segment):
        with wave.open(path, 'r') as w:
            self.ch = w.getnchannels()
            self.width = w.getsampwidth()
            self.fr = w.getframerate()
            self.fn = w.getnframes()
            self.data = w.readframes(self.fn)

        if is_audio_segment:
            self.numpy2AudioSegment()

    # def save_as_wav(data, sample_width, frame_rate, channels, exp_path):
    def save_as_wav(self, export_path):
        """ wave ファイルとして保存 """

        with wave.open(export_path, 'w') as w:
            w.setsampwidth(self.width)
            w.setframerate(self.fr)
            w.setnchannels(self.ch)
            w.writeframes(self.data)

    # def separate_wav(self, path, cut_interval, shift_time):
    def separate_wav(self, cut_interval, shift_time):
        # st = shift_time
        # st = int(shift_time)

        # フレームに応じて図の横幅が変わるため、一定値にする
        # frames = int(self.ch * self.fr * st)
        frames = int(self.ch * self.fr)

        # num_cut = int(self.total_time_int // st)
        # num_cut = self.total_time_int
        # end_condition = frames * num_cut

        sample = frombuffer(self.data, dtype=int16)

        # 実際の frames と変更するため注意
        # => end_condition で配列外参照を防ぐ
        frames = 10000  # 横幅を合わせるため
        interval = cut_interval * 10

        # for i in range(num_cut):
        for i in range(len(sample) // frames):
            bgn = int(i * frames)
            end = int((i + interval) * frames)
            # end = (i + 11) * frames
            """
                (i + 10) => 1 sec.

                画像的に真四角にならないから
                (i + 11) => 1 + N sec.
            """

            # frame を超えたら None
            # if end >= end_condition:
            #     # print('  over frames')
            #     return None

            if end >= len(sample):
                return None

            # cut
            wav_data = sample[bgn:end]

            # generator
            yield wav_data

    # def numpy2AudioSegment(self, data, sample_width, frame_rate, channels):
    def numpy2AudioSegment(self):
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

        self.sound = AudioSegment(
            data=self.data,
            sample_width=self.width,
            frame_rate=self.fr,
            channels=self.ch)

        samples = np.array(self.sound.get_array_of_samples())
        sample = samples[::self.sound.channels]
        self.sound._data = sample

        # wave, audiosegmentの整合性
        # self.data = sample
