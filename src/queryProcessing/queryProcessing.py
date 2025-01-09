import concurrent.futures

import numpy as np
from commonUtilities import commonUtilities
from textProcessing import invertedIndex
from queryProcessing import queryExpansion
from nltk.corpus import wordnet as wn

class QueryProcessing:
    def __init__(self, index: invertedIndex.InvertedIndex) -> None:
        self.queryVector = None
        self.queryTokens = None
        self.allDocumentIds = None
        self.documentsVector = None
        self.index: invertedIndex.InvertedIndex = index
        self.metadata = self.index.getMetadata()

    def processQuery(self, queryString: str) -> None:

        self.queryTokens = self.__createFullQuery(queryString)  # tokenise the query
        self.allDocumentIds = self.__loadDocumentIds()
        self.documentsVector = np.zeros((len(self.queryTokens), len(self.allDocumentIds)))  # create array of vectors for
        self.queryVector = self.queryTfIdf()  # produces a vector representation of the query in relation to the document collection

        print(f'Searching for:{self.queryTokens}')
        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
            executor.map(self.__vectoriseDocuments,[(documentId, column) for column, documentId in enumerate(self.allDocumentIds)])

        similarityScores = sorted(self.findCosineSimilarity(), key=lambda docScorePair: docScorePair[1], reverse=True)

        print(f'from {self.documentsVector.shape[1]}')
        print(self.queryVector)
        for docName, similarity, vec in similarityScores[:30]:
            print(f'{"src/videogames/"+docName.split('/')[-1]} has a similaity of {similarity * 100}%,{vec}')

    def __createFullQuery(self, queryString: str) -> list:
        tokens = commonUtilities.CommonUtilities.tokenizeString(queryString)
        newQueryTokens = queryExpansion.QueryExpansion(self.index,self.metadata).expandQuery(tokens)
        return newQueryTokens

    def __loadDocumentIds(self):
        documentIds = []
        for token in self.queryTokens:  # find all the documents that contain the query tokens
            if bool(self.index[token]):
                for docs in self.index[token]["postings"]:
                    if docs not in documentIds:
                        documentIds.append(docs)  # add the document to the first row of the vectorised query

        return documentIds

    def queryTfIdf(self):  # do idf scoring on the query itself and create a vector
        queryVector = np.zeros((len(self.queryTokens), 1))
        for index, token in enumerate(self.queryTokens):
            tf = 1 + (np.log((self.queryTokens.count(token))))
            idf = self.__inverseDocumentFrequency(token)
            tfIdf = tf * idf
            queryVector[index, 0] = tfIdf
        return queryVector

    def __vectoriseDocuments(self,documentIdColumnPair: tuple[str, int]) -> None:  # documents into vector representation
        documentId, column = documentIdColumnPair
        for row, token in enumerate(self.queryTokens):
            term = token
            if documentId in self.index[term]["postings"]:  # if the term is in the document
                # calculate tf-idf
                tfIdfScore: float = self.__computeIdfScore(documentId, term)
                self.documentsVector[row, column] = tfIdfScore  # add the tf-idf score to the vectorised query
            else:
                self.documentsVector[row, column] = 0  # if the term is not in the document the idf score is 0

    def __computeIdfScore(self, documentId: str,term: str) -> float:  # compute tfidf score on documents with the tokens
        try:
            termFrequency = self.__termFrequency(documentId, term)
            documentFrequency = self.__inverseDocumentFrequency(term)
            metadataAdditionalscore = 30 if term in self.metadata[documentId]["gameInformation"] else 1
            tfIdf = termFrequency * documentFrequency * metadataAdditionalscore
            return tfIdf
        except Exception as e:
            print(e)

    def findCosineSimilarity(self):  # find the cosine similarity between each document and the queries
        # normalise document vectors lengths
        normArray = np.linalg.norm(self.documentsVector, axis=0)
        for index, value in enumerate(normArray):
            if value != 0:
                self.documentsVector[:, index] = self.documentsVector[:, index] / value  # go colllum by collumn

        # normalise query vector
        queryNorm = np.linalg.norm(self.queryVector, axis=0)
        self.queryVector = (self.queryVector / queryNorm) if queryNorm != 0 else self.queryVector

        resultsTuple: list[tuple[str, float,list]] = []

        for index in range(self.documentsVector.shape[1]):
            cosignSimilarity = np.dot(self.queryVector.T, self.documentsVector[:, index])
            resultsTuple.append((self.allDocumentIds[index], cosignSimilarity, self.documentsVector[:, index]))

        return resultsTuple
        # do sclar product for each document on each term

    __termFrequency = lambda self, documentId, term: 1 + np.log(self.index[term]["postings"][documentId]["occurrences"])
    __inverseDocumentFrequency = lambda self, term: 1 + np.log((len(self.metadata) / self.index[term]["totalDocumentFrequency"]))

# vectorised query example for hello world

#         [d1,d2,..dn]
# "hello" [1,0,..0]
# "world" [0,1,..0]

# calculate term frequency 
# calculate inverse document frequency


# can add look t bigrams and add their other words to the query to increase the search results
