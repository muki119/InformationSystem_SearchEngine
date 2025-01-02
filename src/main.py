import cProfile
import pstats

from textProcessing import indexer
from queryProcessing import queryProcessing


def main():
    ins = indexer.Indexer('src/wordIndex.pk1')
    #ins.buildIndex()
    queryProcess = queryProcessing.QueryProcessing(ins.getIndex())
    queryProcess.processQuery("zatch bell super fighting game")
    

if __name__ == "__main__":
    cProfile.run('main()', 'profile_output')
    p = pstats.Stats('profile_output')
    p.sort_stats('cumulative').print_stats(30)