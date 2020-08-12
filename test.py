import argparse
import sys


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("-reg", "--region", nargs='+', default=['balakovo'],
                        help="request for parse example: beauty_large, beauty_small, beauty_msk_mo or '[msk, ...]'")
    return parser


def main():
    parser = create_parser()
    namespace = parser.parse_args()
    b = 0
    for i in namespace.region:
        print(i)
        if i == 'a':
            b = ['suka nahui bliat', 'jopa']
    for i in b:
        print(i + 'test')
    print(namespace.region)
    return print(b)


if __name__ == '__main__':
    main()
