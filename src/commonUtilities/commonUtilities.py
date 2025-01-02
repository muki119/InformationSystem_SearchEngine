import re
import spacy
class CommonUtilities:
    _textRegex = re.compile(r"[\|:!-,]|\t+|[^\w](\.)+")
    _nlp = spacy.load("en_core_web_sm",disable=["textcat","ner"])
    @staticmethod
    def tokenizeString(inputText:str)->list[str]:
        inputText =CommonUtilities._textRegex.sub('',inputText)
        return [t.lemma_.strip() for t in CommonUtilities._nlp(inputText) if not t.is_stop and len(t)>1] 