from typing import AsyncContextManager
from pydub import AudioSegment
import utils as ul
import sys
import numpy as np


def main():
    argv = sys.argv
    sound = ul.load_wav(argv[1])
    sample = sound._data

    ch = sound.channels
    width = sound.sample_width
    rate = sound.frame_rate
    frame_width = sound.frame_width
    frame_count = sound.frame_count()

    frame_num = frame_width * frame_count
    total_time = 1.0 * frame_num / rate
    total_time_int = int(total_time)
    # t = time
    shift_time = 0.1  # <- arg
    t = shift_time
    frames = int(ch * rate * t)
    num_cut = int(total_time_int // t)

    print(f'channel: {ch}')
    print(f'sample width: {width}')
    print(f'frame rate: {rate}')
    print(f'frame num: {frame_num}')
    print(f'total time: {total_time}')
    print(f'total time(int): {total_time_int}')
    print(f'shift time: {shift_time}')
    print(f'frames: {frames}')
    print(f'number of cut: {num_cut}')
    print(f'sample: {sample}')

    # 音の長さを一定にするため（フレームレートによって音の長さが変わる）
    frames = 10000

    print(len(sample))
    # sample * channel
    # sample2 = sample * ch
    sample2 = np.ndarray.flatten(sample)
    # print(type(sample[0]))
    # sample2 = np.concatenate(sample)

    # temp = []
    print(len(sample))
    # for i in sample:
        # for j in i:
        #     temp.append(j)
        # print(type(i))

    # sample2 = np.array(temp)

    # print(len(sample2))
    # print(sample == sample2)
    for it in range(num_cut):
        begin_time = it * frames
        # end_time =


if __name__ == '__main__':
    main()
