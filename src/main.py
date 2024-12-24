import bs4;
import pickle;
import numpy;
from textProcessing import indexer
import cProfile
import pstats


def main():
    indexer.Indexer('src/wordIndex.pk1').buildIndex()

if __name__ == "__main__":
    cProfile.run('main()', 'profile_output')
    p = pstats.Stats('profile_output')
    p.sort_stats('cumulative').print_stats(20)