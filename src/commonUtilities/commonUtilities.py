import re
import spacy
import nltk
from nltk import PorterStemmer
from nltk.corpus import stopwords

class CommonUtilities:
    _textRegex = re.compile(r"[\|:!-,]|\t+|[^\w](\.)+")
    _porterStemmer = PorterStemmer()
    _stopwords = set(stopwords.words('english'))
    _nlp = spacy.load("en_core_web_sm",disable=["textcat"])
    @staticmethod
    def tokenizeString(inputText:str)->list[str]:
        inputText =CommonUtilities._textRegex.sub('',str(inputText)).lower() # remove  unnecessary characters
        documentTokens = CommonUtilities._nlp(inputText) # tokenize the string
        tokens = [t.lemma_.strip() for t in documentTokens if not t.is_stop and len(t.lemma_.strip())>1]
        return tokens
    @staticmethod
    def stemmedTokenizeString(inputText:str)->list[str]:
        inputText =CommonUtilities._textRegex.sub('',str(inputText)).lower() # remove  unnecessary characters
        documentTokens = nltk.wordpunct_tokenize(inputText)# tokenize the string
        tokens = [CommonUtilities._porterStemmer.stem(t).strip() for t in documentTokens if not t in CommonUtilities._stopwords  and len(CommonUtilities._porterStemmer.stem(t).strip())>1]
        return tokens

# experiment wih stemming and lemmitisation
#look at accuracy of them