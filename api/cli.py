import argparse
import os

from repo.Zipfile import Zipfile

######
#ARGS#
######
parser = argparse.ArgumentParser(
    description='Zip static analyzer',
    usage='python main.py ZIPFILE [-h] [-s] [-l]'
)

parser.add_argument(
    'src',
    metavar='ZIPFILE',
    help='The zip file to be analyzed'
)

parser.add_argument(
    '-s',
    '--short',
    required=False,
    help='prints a short version of the zip analyzation',
    action="store_true"
)

parser.add_argument(
    "-l",
    "--long",
    required=False,
    action="store_true",
    help="prints a long version of the zip analyzation"
)


def main():
    args = parser.parse_args()
    if args.short and args.long or not os.path.isfile(args.src):
        return print("You can't print a long and a short information")
    print_type = "long" if args.long else ("short" if args.short else None)
    return print(Zipfile(args.src, print_type))

if __name__ == "__main__":
    main()
