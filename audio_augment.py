import numpy as np
# import librosa


class AudioAugmentation:
    def __init__(self):
        pass

    def append_white_noise(self, data, noise_ratio=4000):
        """
        ホワイトノイズ付加
        """

        # ノイズ生成
        noise = np.random.randn(len(data))

        # ノイズ付加
        augmented_data = data + (noise_ratio * noise)
        augmented_data = augmented_data.astype(type(data[0]))

        return augmented_data
