import argparse
import logging

from pairpricing import PairPricing

logger = logging.getLogger(__name__)

def _parse_args():
    parser = argparse.ArgumentParser(description='Check the availability and pricing of free/paid pairs on the Google Play Store')

    parser.add_argument('pairscsv', metavar='PAIRSCSV', help='Path to a CSV of free,paid pairs, one pair per line')
    parser.add_argument('--verbose', '-v', action='store_true', help='Enable verbose logging')

    return parser.parse_args()

if __name__ == '__main__':
    args = _parse_args()

    if(args.verbose):
        logging.basicConfig(level=logging.INFO)
    else:
        logging.basicConfig()

    with open(args.pairscsv, 'r') as pair_file:
        for line in pair_file:
            (free, paid) = line.strip().split(',')
            pair = PairPricing(free, paid)

            print(pair)
