import pyaudio
import wave
import numpy as np
from pydub import AudioSegment
from util import Util

from util import is_debug  # for debug


class Record:
    """ 録音する """

    def __init__(self):

        util = Util()

        # ファイル形式
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 1
        self.RATE = 44100
        self.CHUNK = 2 ** 1
        self.RECORD_SEC = 1
        self.SAMPLE_WIDTH = 2

        # 録音データを保存するか
        self.is_save_file = util.is_save_file

        if self.is_save_file:
            # 出力先フォルダの作成
            util.make_dir(util.export_path)
            self.save_path = f'{util.export_path}/file.wav'

        # 録音開始
        self.audio = pyaudio.PyAudio()
        self.stream = self.audio.open(
            format=self.FORMAT,
            channels=self.CHANNELS,
            rate=self.RATE,
            input=True,
            input_device_index=1,
            frames_per_buffer=self.CHUNK)

    def record(self):
        """ 録音する

        Returns
        -------
        self.save_path : str, if self.is_save_file is True
            保存先のパス
        frame_data : numpy.ndarray, if self.is_save_file is False
            音データ
        """

        if is_debug:
            print('recodng...')  # for debug

        frames = []
        for _ in range(0, int(self.RATE / self.CHUNK * self.RECORD_SEC)):
            # オーバーフローは無視
            frame_data = self.stream.read(self.CHUNK, exception_on_overflow=False)
            frames.append(frame_data)

        if is_debug:
            print('finished recording', end='')
            if self.is_save_file:
                print(f', save to {self.save_path}', end='')
            print()

        # フレームを連結
        frame_data = b''.join(frames)

        # 保存するなら, 書き出して保存先パスを返す
        if self.is_save_file:
            self.save_data_as_wav(self.audio, frame_data)
            return self.save_path

        # bytesからnumpy配列にする
        frame_data = np.frombuffer(frame_data, dtype='int16')
        return frame_data

    def load_wav(self, wav_path):
        """ wavファイルを読み込む

        Parameters
        ----------
        wav_path : str
            wavファイルのパス

        Returns
        -------
        sound : pydub.audio_segment.AudioSegment
            音の情報
        """

        # 読み込み
        sound = AudioSegment.from_wav(wav_path)

        # サンプルデータ取得
        samples = np.array(sound.get_array_of_samples())
        sample = samples[::sound.channels]
        sound._data = sample

        return sound

    def save_data_as_wav(self, audio, frame_data):
        """ データをwav形式で保存する

        Parameters
        ----------
        audio : pyaudio.PyAudio
            保存ファイルの情報
        frame_data : bytes
            音データ
        """

        with wave.open(self.save_path, 'wb') as wav:
            wav.setnchannels(self.CHANNELS)
            wav.setsampwidth(audio.get_sample_size(self.FORMAT))
            wav.setframerate(self.RATE)
            wav.writeframes(frame_data)

    def numpy2AudioSegment(self, data):
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
            sample_width=self.SAMPLE_WIDTH,
            frame_rate=self.RATE,
            channels=self.CHANNELS)

        return sound
