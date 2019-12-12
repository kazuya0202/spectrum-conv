import wave
import struct
import math
import os
import sys
from scipy import int16, frombuffer

export_dir = 'export'


def cut_wav(filename, time):
    wav_file = f'{filename}.wav'
    wr = wave.open(wav_file, 'r')

    ch = wr.getnchannels()
    width = wr.getsampwidth()
    fr = wr.getframerate()
    fn = wr.getnframes()
    total_time = 1.0 * fn / fr
    integer = math.floor(total_time)
    # t = int(time)
    t = time

    # フレームに応じて図の横幅が変わるため、一定値にする
    frames = int(ch * fr * t)
    # frames = 10000  # 数値はかえてもおけ (下に書く

    num_cut = int(integer // t)

    print(f'channle: {ch}')
    print(f'sample width: {width}')
    print(f'frame rate: {fr}')
    print(f'frame num: {fn}')
    print(f'params: {wr.getparams()}')
    print(f'total time: {total_time}')
    print(f'total time(int): {integer}')
    print(f'time: {t}')
    print(f'frames: {frames}')
    print(f'number of cut: {num_cut}')

    data = wr.readframes(wr.getnframes())
    wr.close()
    X = frombuffer(data, dtype=int16)

    out_file_path = f'{export_dir}/{filename}'
    if not os.path.exists(out_file_path):
        os.makedirs(out_file_path)

    end_condition = frames * num_cut

    filename = os.path.basename(filename)

    frames = 10000  # 横幅を合わせるための
    for i in range(num_cut):
        print(i)

        out_file = f'{out_file_path}/{filename}_{i}.wav'
        start_cut = i * frames
        end_cut = (i+10) * frames + frames

        # print(start_cut, end_cut)
        if end_cut > end_condition:
            print('  over frames')
            return

        Y = X[start_cut:end_cut]
        out_date = struct.pack('h' * len(Y), *Y)

        # output
        with wave.open(out_file, 'w') as ww:
            ww.setnchannels(ch)
            ww.setsampwidth(width)
            ww.setframerate(fr)
            ww.writeframes(out_date)


def main(path='crossing1'):
    argv = sys.argv
    isfile = False

    if len(argv) >= 2:
        path = argv[1]

    if path.find('.') > -1:
        isfile = True
        path = path[:path.find('.')]
    print(path)

    if not os.path.exists(f'{export_dir}/{path}'):
        os.makedirs(f'{export_dir}/{path}')

    cut_time = 0.1

    # if os.path.isfile(path):
    if isfile:
        cut_wav(path, cut_time)

    else:
        for (root, dirs, files) in os.walk(path):
            for f in files:
                cut_wav(f'{root}{os.path.splitext(f)[0]}', cut_time)


if __name__ == '__main__':
    main()
