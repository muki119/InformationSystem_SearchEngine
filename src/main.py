import bs4;
import pickle;
import numpy;
from textProcessing import indexer




if __name__ == "__main__":
    indexer.Indexer('src/wordIndex.pk1').buildIndex()