import cProfile
import pstats

from textProcessing import indexer
from queryProcessing import queryProcessing
from queryProcessing import queryExpansion
from commonUtilities.commonUtilities import CommonUtilities


def main():
    ins = indexer.Indexer('src/wordIndex.pk1')
    # ins.buildIndex()
    queryProcess = queryProcessing.QueryProcessing(ins.getIndex())
    queryProcess.processQuery("50 cent fighting games")
    # while True:
    #     query = str(input("Input query: ")).strip()
    #     print(CommonUtilities.tokenizeString(query))

if __name__ == "__main__":
    cProfile.run('main()', 'profile_output')
    p = pstats.Stats('profile_output')
    p.sort_stats('cumulative').print_stats(30)