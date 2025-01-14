import concurrent.futures
import sys
import traceback
import numpy as np
from commonUtilities import commonUtilities
from textProcessing import invertedIndex
from queryProcessing import queryExpansion
from nltk.corpus import wordnet as wn


class QueryProcessing:
    def __init__(self, index: invertedIndex.InvertedIndex, stemmed=False,expansion = False) -> None:
        self.queryVector = None
        self.expansion = expansion
        self.stemmed: bool = stemmed
        self.queryTokens = None
        self.allDocumentIds = None
        self.documentsVector = None
        self.index: invertedIndex.InvertedIndex = index
        self.metadata = self.index.getMetadata()

    def processQuery(self, queryString: str) -> list[tuple[str, float, list[int]]]:
        """Processes a given query , expanding it if possible and returning the most """
        try:
            self.queryTokens = self.__createFullQuery(queryString,self.stemmed)  # tokenise the query
            self.allDocumentIds = self.__loadDocumentIds()  #load all the documents that contain any of the tokens
            if len(self.queryTokens) == 0 or len(self.allDocumentIds) == 0:
                return []
            self.documentsVector = np.zeros((len(self.queryTokens), len(self.allDocumentIds)))  # where document vectors are stored
            self.queryVector = self.queryTfIdf()  # produces a vector representation of the query in relation to the document collection

            print(f'Searching for:{self.queryTokens}')
            with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
                executor.map(self.__vectoriseDocuments,[(documentId, column) for column, documentId in enumerate(self.allDocumentIds)])

            similarityScores = sorted(self.__findCosineSimilarity(), key=lambda docScorePair: docScorePair[1],reverse=True)

            print(f'From {self.documentsVector.shape[1]} Documents:')
            print(f'{self.queryVector}')
            return similarityScores[:]
        except Exception as ex:
            print(ex)
            return []

    def __createFullQuery(self, queryString: str, stemmer=False) -> list[str]:
        try:
            lemmatizedTokens = commonUtilities.CommonUtilities.tokenizeString(queryString)
            stemmedTokens = commonUtilities.CommonUtilities.stemmedTokenizeString(queryString)
            newQueryTokens = queryExpansion.QueryExpansion(self.index, self.metadata).expandQuery(lemmatizedTokens if not stemmer else stemmedTokens)  #expands the query and adds extra tokens for recall
            return (lemmatizedTokens if not stemmer else stemmedTokens) if not self.expansion else newQueryTokens
        except Exception as ex:
            print("Error while creating query", ex)
            return []

    def __loadDocumentIds(self) -> list[str]:
        documentIds = []
        try:
            for token in self.queryTokens:  # find all the documents that contain the query tokens
                if bool(self.index[token]):
                    for docs in self.index[token]["postings"]:
                        if docs not in documentIds:
                            documentIds.append(docs)  # add the document to the first row of the vectorised query
                else:
                    self.queryTokens.remove(token)  #if token cannot be found in index then remove it
            return documentIds
        except Exception as e:
            print("Error loading documentIds: ", e)
            return []

    def queryTfIdf(self):  # do idf scoring on the query itself and create a vector
        try:
            queryVector = np.zeros((len(self.queryTokens), 1))
            for index, token in enumerate(self.queryTokens):
                if not bool(self.index[token]):
                    return 1
                tf = 1 + (np.log((self.queryTokens.count(token))))
                idf = self.__inverseDocumentFrequency(token)
                tfIdf = tf * idf
                queryVector[index, 0] = tfIdf
            return queryVector
        except Exception as e:
            print("Error while trying to produce TfIdf scores for query : ", e)

    def __vectoriseDocuments(self,documentIdColumnPair: tuple[str, int]) -> None:  # documents into vector representation
        try:
            documentId, column = documentIdColumnPair
            for row, token in enumerate(self.queryTokens):
                term = token
                if documentId in self.index[term]["postings"]:  # if the term is in the document
                    # calculate tf-idf
                    tfIdfScore: float = self.__computeIdfScore(documentId, term)
                    self.documentsVector[row, column] = tfIdfScore  # add the tf-idf score to the vectorised query
                else:
                    self.documentsVector[row, column] = 0  # if the term is not in the document the idf score is 0
        except Exception as e:
            print("Error while trying to vectorise documents: ", e)

    def __computeIdfScore(self, documentId: str,term: str) -> float:  # compute tfidf score on documents with the tokens
        try:
            metadataAdditionalscore =3 if term in self.metadata[documentId]["gameInformation"] else 1
            termFrequency = self.__termFrequency(documentId, term, metadataAdditionalscore)
            documentFrequency = self.__inverseDocumentFrequency(term, metadataAdditionalscore)
            tfIdf = termFrequency * documentFrequency
            return tfIdf
        except Exception as e:
            print("Error while trying to compute tfIdf score for documents: ", e)
            return 1

    def __findCosineSimilarity(self):  # find the cosine similarity between each document and the queries
        # normalise document vectors lengths
        normArray = np.linalg.norm(self.documentsVector, axis=0)
        for index, value in enumerate(normArray):
            if value != 0:
                self.documentsVector[:, index] = np.divide(self.documentsVector[:, index],
                                                           value)  # go colllum by collumn

        # normalise query vector
        queryNorm = np.linalg.norm(self.queryVector, axis=0)
        self.queryVector = np.divide(self.queryVector, queryNorm[0]) if queryNorm != 0 else self.queryVector
        resultsTuple: list[tuple[str, float, list]] = []

        for index in range(self.documentsVector.shape[1]):
            cosignSimilarity = np.dot(self.queryVector.T, self.documentsVector[:, index])
            resultsTuple.append((self.allDocumentIds[index], cosignSimilarity, self.documentsVector[:, index]))

        return resultsTuple
        # do sclar product for each document on each term

    __termFrequency = lambda self, documentId, term, metaDataScore=1: (1 + np.log(
        self.index[term]["postings"][documentId]["occurrences"])) * metaDataScore
    __inverseDocumentFrequency = lambda self, term, metaDataScore=1: (1+np.log(
        (len(self.metadata) / (self.index[term]["totalDocumentFrequency"]+1)) ) ) * metaDataScore

# vectorised query example for hello world

#         [d1,d2,..dn]
# "hello" [1,0,..0]
# "world" [0,1,..0]

# calculate term frequency 
# calculate inverse document frequency


# can add look t bigrams and add their other words to the query to increase the search results
