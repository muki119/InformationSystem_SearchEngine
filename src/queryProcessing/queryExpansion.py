import concurrent.futures
from nltk.corpus import wordnet as wn
import numpy as np
import spacy


class QueryExpansion:
    _nlp = spacy.load('en_core_web_sm')
    def __init__(self,index,metadata):
        self.additionalNouns = None
        self.__index = index
        self.__metadata = metadata

    def expandQuery(self, tokenizedQuery):
        queryNouns = self._nlp.pipe(tokenizedQuery)
        nouns = []
        for doc in queryNouns:
            for tokens in doc:
                if tokens.pos_ == "NOUN":
                    nouns.append(tokens.lemma_.lower())
        self.additionalNouns = []
        for noun in nouns:
            chosenSynonym = self.__findNounSynonyms(noun)
            if bool(chosenSynonym):
                self.additionalNouns.append(chosenSynonym)
        print(f'Expanded with {self.additionalNouns}')

        return tokenizedQuery+self.additionalNouns
    def __findNounSynonyms(self,nounWord):
        """Finds the noun synonyms and ranks them from most to least relevant using tf-Idf ranking"""
        synonymsOfWord = set()
        for lemma in wn.synsets(nounWord, pos=wn.NOUN):
            for lemmas in lemma.lemmas():
                synonym = lemmas.name()
                if bool(self.__index[synonym]) and synonym not in nounWord:
                    synonymsOfWord.add(synonym) # gets all the synonyms of a given word and adds it to a set of synonyms
        return self.__synonymRanking(synonymsOfWord) #return the highest ranking synonym for that word

    def __synonymRanking(self,synonymsOfWord):
        """Given a noun Word it,returns the highest ranking synonym for a given word """
        synonymsScorePair = []
        for synonym in synonymsOfWord:
            tf = 1 # always going to be log(1) because its a set
            idf = 1 + np.log((len(self.__metadata) / self.__index[synonym]["totalDocumentFrequency"]))
            tfIdfScore = tf*idf
            synonymsScorePair.append((synonym, tfIdfScore))
        rankedSynonyms =  sorted(synonymsScorePair, key= lambda x: x[1],reverse=True)
        if len(rankedSynonyms) != 0:
            return rankedSynonyms[0][0]
        else:
            return None