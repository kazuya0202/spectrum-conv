from pydub import AudioSegment
import wave
import numpy as np
from PIL import Image


def has_elems_in_list(_list, elms):
    """ リスト内に要素が含まれているかどうか """
    if isinstance(_list, list) or isinstance(_list, tuple):
        res = [True if elm in _list else False for elm in elms]
        return any(res)

    return elms in _list


def load_wav(wav_path):
    """ wavファイルを読み込む """

    # 読み込み
    sound = AudioSegment.from_wav(wav_path)

    # サンプルデータ取得
    samples = np.array(sound.get_array_of_samples())
    sample = samples[::sound.channels]
    sound._data = sample

    return sound


def crop_img(crop_range, img_path):
    """ 画像を切り取る """

    img = Image.open(img_path)  # 保存
    img_crop = img.crop(crop_range)  # 切り取り
    img_crop.save(img_path)  # 保存


def save_as_wav(data, sample_width, frame_rate, channels, exp_path):
    """ wave ファイルとして保存 """

    with wave.open(exp_path, 'w') as w:
        w.setsampwidth(sample_width)
        w.setframerate(frame_rate)
        w.setnchannels(channels)
        w.writeframes(data)


def numpy2AudioSegment(data, sample_width, frame_rate, channels):
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

    samples = np.array(sound.get_array_of_samples())
    sample = samples[::sound.channels]
    sound._data = sample

    return sound
