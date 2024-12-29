import cProfile
import pstats

from textProcessing import indexer
from queryProcessing import queryProcessing


def main():
    ins = indexer.Indexer('src/wordIndex.pk1')
    #ins.buildIndex()
    queryProcess = queryProcessing.queryProcessing(ins.getIndex())
    queryProcess.processQuery("50 cent ")
    

if __name__ == "__main__":
    cProfile.run('main()', 'profile_output')
    p = pstats.Stats('profile_output')
    p.sort_stats('cumulative').print_stats(30)