import wave
from dataclasses import dataclass
from typing import Any

import numpy as np
from pydub import AudioSegment
from scipy import frombuffer, int16


@dataclass
class SoundInfo:
    data: Any = None  # data
    channels: int = 1  # channels
    width: int = 2  # sample width
    f_rate: int = 44100  # frame rate
    f_num: int = 1  # frame num

    def __post_init__(self):
        self.total_time: float = 1.0 * self.f_num / self.f_rate
        self.total_time_int: int = int(np.floor(self.total_time))

        self.sound: AudioSegment = None

    def show_info(self):
        print(f"channels    : {self.channels}")
        print(f"sample width: {self.sample_width}")
        print(f"frame rate  : {self.frame_rate}")
        print(f"frame num   : {self.frame_num}")

    def update(self, **options):
        self.channels = options.pop("channels", self.channels)
        self.sample_width = options.pop("sample_width", self.sample_width)
        self.frame_rate = options.pop("frame_rate", self.frame_rate)
        self.frame_num = options.pop("frame_num", self.frame_num)

        self.__post_init__()

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
            data=self.data, sample_width=self.width, frame_rate=self.f_rate, channels=self.channels,
        )

        samples = np.array(self.sound.get_array_of_samples())
        sample = samples[:: self.sound.channels]
        self.sound._data = sample
        # def save_as_wav(data, sample_width, frame_rate, channels, exp_path):

    def save_as_wav(self, export_path):
        """ wave ファイルとして保存 """

        with wave.open(export_path, "w") as w:
            w.setsampwidth(self.width)
            w.setframerate(self.f_rate)
            w.setnchannels(self.channels)
            w.writeframes(self.data)


@dataclass
class SeparateWave:
    s_info: SoundInfo
    is_load_wave: bool = True
    is_audio_segment: bool = False

    def __post_init__(self):
        if self.s_info.data is None:
            return

        if self.is_load_wave:
            self.s_info = self.load_wav(self.s_info.data, self.is_audio_segment)

    def load_wav(self, path, is_audio_segment: bool):
        with wave.open(path, "r") as w:
            ch = w.getnchannels()
            width = w.getsampwidth()
            fr = w.getframerate()
            fn = w.getnframes()
            data = w.readframes(fn)

            si = SoundInfo(data, ch, width, fr, fn)

        if is_audio_segment:
            si.numpy2AudioSegment()

        return si

    # def save_as_wav(data, sample_width, frame_rate, channels, exp_path):
    def save_as_wav(self, export_path):
        """ wave ファイルとして保存 """

        with wave.open(export_path, "w") as w:
            w.setsampwidth(self.s_info.width)
            w.setframerate(self.s_info.f_rate)
            w.setnchannels(self.s_info.channels)
            w.writeframes(self.s_info.data)

    # def separate_wav(self, path, cut_interval, shift_time):
    def separate_wav(self, cut_interval, shift_time):
        frames = int(self.s_info.channels * self.s_info.f_rate)
        shift_frames = int(frames * shift_time)

        sample = frombuffer(self.s_info.data, dtype=int16)
        delimiter = len(sample) // shift_frames  # delimit step

        for i in range(delimiter):
            bgn = i * shift_frames
            end = int(bgn + frames * cut_interval)

            if end >= len(sample):
                return None

            wav_data = sample[bgn:end]  # cut
            yield wav_data  # generator
