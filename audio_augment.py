import numpy as np

# import librosa


class AudioAugmentation:
    def append_white_noise(self, data, percent=10):
        """
        ホワイトノイズ付加
        """

        # ノイズ生成
        noise = np.random.randn(len(data))
        coef = np.max(data) * (percent / 100)  # ノイズの係数

        # ノイズ付加
        augmented_data = data + (coef * noise)
        augmented_data = augmented_data.astype(type(data[0]))

        return augmented_data
