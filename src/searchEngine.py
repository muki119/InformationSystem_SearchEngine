import datetime
import os
import re

from matplotlib import pyplot as plt

from queryProcessing.queryProcessing import QueryProcessing
from textProcessing import indexer


class SearchEngine:
    def __init__(self,stemmed = False,expansion = False):
        """Stemmed - Determines if the words in index are stemmed or lemmatized - False as default\n
            Expansion - determines if query expansion is to be used - False as default
        """
        try:
            self.stemmed = stemmed
            self.expansion = expansion
            self.indexManager = indexer.Indexer('src/data/',stemmed)
            self.indexManager.buildIndex()
            self.queryProcess = QueryProcessing(self.indexManager.getIndex(),stemmed,expansion)
            print(len(self.indexManager.getIndex()))
        except Exception as e:
            print(e)
            exit(1)

    def search(self):
        while True:
            try:
                query = str(input("Ask away ::"))
                results = self.queryProcess.processQuery(query)
                if not results:
                    print(f'No results for query:{query}')
                    continue
                self.printResults(results)
                self.saveResults(re.sub(r'[\s\\]',"_",query),results)
                self.displayResults(query,results)
            except Exception as e:
                print(e)
    def displayResults(self,query,results):
        y = [val[1] for val in results]
        x = list(range(1,len(y)+1))

        plt.rcParams["figure.figsize"] = [12.80, 7.2]
        plt.rcParams["figure.autolayout"] = True
        plt.xlabel("Rankings")
        plt.ylabel("Cosine Similarity Score")
        plt.title(f'Cosine Similarity Score graph for {query} , {"stemmed" if self.stemmed else "Lemmatised"},{"Expanded" if self.expansion else "Not expanded"})')
        plt.plot(x, y, color="red")
        plt.grid()
        plt.show()

    def printResults(self, resultList):
        for rank , val  in enumerate(resultList):
            docName, similarity, vec = val
            print(f'"{rank+1}:{"src/videogames/"+docName.split('/')[-1]}":\n\tHas a similaity of {similarity * 100}%\n{vec}')

    def saveResults(self,queryString=None,resultList=None):
        if not os.path.exists('src/results/'):
            os.makedirs('src/results/')
        dateTime = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
        with open(f'src/results/{queryString}{dateTime}.txt', 'w') as outfile:
            for rank , val in enumerate(resultList):
                docName, similarity, vec = val
                outfile.write(f'{rank+1}:{"src/videogames/"+docName.split('/')[-1]}:{similarity}\n')
