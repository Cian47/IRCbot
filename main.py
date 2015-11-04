import argparse
from ircbot import *

def main(args):
    bot = IRCbot(args)
    pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbose", action="store_true", help="be verbose")
    parser.add_argument("-s", "--server", type=int, help="which servernr to connect to", required=False, default=1)
    parser.add_argument("--hello", action="store_true", help="testmod")
    args=parser.parse_args()
    main(args)
