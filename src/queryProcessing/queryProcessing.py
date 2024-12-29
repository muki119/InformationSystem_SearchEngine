#should 
# take in a query
# should then tokenize and lemmitize the query
# then should look thriugh index and do tf-idf calculations
# then should return the top 10 results
import spacy
import re
import numpy as np
import pickle
import concurrent.futures
from textProcessing import invertedIndex

#multithreaded to find all the documents that contain the query tokens

#class to process the query and return the top 10 results
class queryProcessing():
    __textRegex = re.compile(r"[\|:!-,]|\t+|[^\w](\.)+")
    __nlp = spacy.load("en_core_web_sm")
    
    def __init__(self,index:invertedIndex.InvertedIndex)->None:
        self.index:invertedIndex.InvertedIndex = index
        self.metadata = self.index.getMetadata()
           
    def processQuery(self,inputQuery:str)->None:
        self.queryTokens = self.__tokenizeQuery(inputQuery) # tokenise the query
        allDocumentIds = []
        for token in self.queryTokens: # find all the documents that contain the query tokens
            for docs in self.index[token]["postings"]:
                if docs not in allDocumentIds:
                    allDocumentIds.append(docs) # add the document to the first row of the vectorised query
        
        self.queryVectorised  = np.zeros((len(self.queryTokens),len(allDocumentIds)))#[[] for i in range(len(self.queryTokens))]# create a vectorised query
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
            executor.map(self.__vectoriseQuery,[(documentId,collumn) for collumn,documentId in enumerate(allDocumentIds)])
        print(self.queryVectorised)
            
                
    def __vectoriseQuery(self,documentIdCollumnPair:tuple[str,int])->None:
        documentId,collumn = documentIdCollumnPair
        for row,token in enumerate(self.queryTokens):
            term = token
            if documentId in self.index[term]["postings"]:
                # calculate tf-idf
                tfIdfScore = self.__computeScore(documentId,term)
                self.queryVectorised[row][collumn] = tfIdfScore #add the tf-idf score to the vectorised query
                pass
            else:
                self.queryVectorised[row][collumn] = 0 #if the term is not in the document add 0


    def __tokenizeQuery(self,inputQuery:str)->list[str]:
        inputQuery =self.__textRegex.sub('',inputQuery)
        return [t.lemma_.strip() for t in self.__nlp(inputQuery) if not t.is_stop and len(t)>1]

    def __computeScore(self,documentId:str,term:str)->float:
        termFrequency = self.__termFrequencyWeight(documentId,term)
        documentFrequency = self.__documentFrequencyWeight(term)
        
        tfIdf = termFrequency*documentFrequency
        
        return tfIdf #placeholder
        
    def __termFrequencyWeight(self,documentId:str,term:str):
        termFrequency = self.index[term]["postings"][documentId]["occurrences"] # how many times the term appears in the document
        totalDocumentWords = self.index.metadata[documentId]["totalWords"] # total number of words in the document
        
        return 1+np.log10((termFrequency/totalDocumentWords))
    
    def __documentFrequencyWeight(self,term:str):
        
        return np.log10(self.index[term]["totalDocumentFrequency"]/len(self.index.metadata.keys()))
# vectorised query example for hello world 

#         [d1,d2,..dn]
# "hello" [1,0,..0]
# "world" [0,1,..0]

# calculate term frequency 
#calculate inverse document frequency 


#can add look t bigrams and add their other words to the query to increase the search results