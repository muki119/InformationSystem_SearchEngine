import re
import spacy
class CommonUtilities:
    _textRegex = re.compile(r"[\|:!-,]|\t+|[^\w](\.)+")
    _nlp = spacy.load("en_core_web_sm",disable=["textcat,tagger"])
    @staticmethod
    def tokenizeString(inputText:str)->list[str]:
        inputText =CommonUtilities._textRegex.sub('',str(inputText)).lower()
        documentTokens = CommonUtilities._nlp(inputText)
        return [t.lemma_.strip().lower() for t in documentTokens if not t.is_stop and len(t)>1]

# experiment wih stemming and lemmitisation
#look at accuracy of them