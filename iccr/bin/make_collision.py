import argparse
from iccr import Collision

def do_(galaxy1, galaxy2, pericenter):
    a = Collision(galaxy1, galaxy2).initial_condition_file(pericenter=pericenter)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("galaxy1_name", help="Name of the first galaxy.")
    parser.add_argument("galaxy2_name", help="Name of the second galaxy.")
    parser.add_argument("pericenter", type=float, help="Pericenter distance.")

    args = parser.parse_args()
    do_(args.galaxy1_name, args.galaxy2_name, args.pericenter)
