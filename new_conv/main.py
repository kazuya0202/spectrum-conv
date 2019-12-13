import sys
import utils as ul
from spectrum_conv import SpectrumConvertion


class Main:
    def __init__(self):
        self.sc = SpectrumConvertion()

    def main(self):
        argv = sys.argv

        if ul.has_elems_in_list(argv, ['-h', '--help']):
            print('Usage:')
            print('  python <this-file>.py **/*.wav')
            print('  python <this-file>.py <audio_file>.wav')
            print('  python <this-file>.py')
            exit()

        if ul.has_elems_in_list(argv, ['-t', '--test']):
            print('It specified a \'test\' option.')
            exit()

        if len(argv) == 1:
            fpath = input('> Enter file path: ')
            argv.append(fpath)

        # remove <script>.py to ignore
        argv.remove(argv[0])

        self.sc.main(argv)


if __name__ == '__main__':
    m = Main()
    exit_status = m.main()

    sys.exit(exit_status)
