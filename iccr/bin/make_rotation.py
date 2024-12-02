import argparse
from iccr import Collision


def do_(name1, name2, gal, sequence, angle):
    Collision(name1, name2).do_rotation(gal, sequence, angle)
    print("Done")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("name1", help="Data file.")
    parser.add_argument("name2", help="Data file.")
    parser.add_argument("gal", type=int, help="Data file.")
    parser.add_argument("sequence", type=str, help="Data file.")
    parser.add_argument("--angles", nargs='+', type=float, help="Data file.")
    args = parser.parse_args()
    do_(args.name1, args.name2, args.gal, args.sequence, args.angles)
