import argparse
import os

from Zipfile import Zipfile

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
    help="prints a short version of the zip analyzation"
)



def main() -> None:
    args = parser.parse_args()
    if args.short and args.long or not os.path.isfile(args.src):
        raise argparse.ArgumentError(argument=None,message="U STUPID")
    if args.long:
        return print(Zipfile(args.src))
    if args.short:
        zf = Zipfile(args.src)
        return print(zf.short_str())
    zf = Zipfile(args.src)
    bomb = zf.is_zipbomb()
    if bomb:
        return print("It's a bomb!")
    return print("It's not a bomb")



if __name__ == "__main__":
    main()