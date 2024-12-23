import bs4
import nltk
import spacy
from collections import Counter
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import re
from textProcessing import invertedIndex
class Indexer():
    def __init__(self,path:str):
        self.nlp = spacy.load("en_core_web_sm")
        self.index = invertedIndex.InvertedIndex(path)
        
    def buildIndex(self):
        videogamesLine:str=None
        with open('src/videogame-labels.csv') as videogameLabels :
            videogamesLine = videogameLabels.readlines()[1:]#ignore first line which is just formatting  
        print("Reading and Proccessing files...")
        for pageLineInfo in videogamesLine: # open each page and create its tokens
            pageData = pageLineInfo.rstrip().split(",")
            pageText:str = self.__openPage(pageData)
            tokenFreqdist:list[tuple[any,int]] = self.createTokens(pageText)#dictionary of tokens and their frequency
            for token , freq in tokenFreqdist.items():
                self.index.addWord(token,pageData[0],freq,[1,2,4,5,6])
        self.index.displayDictionary()
        self.index.dumpDictionary()
        print("Done")
        
    def __openPage(self,pageLineInfo:list[str])->str:
        # url,STRING : esrb,STRING : publisher,STRING : genre,STRING : developer
        var1  = pageLineInfo[0].split("/")
        pageurl = "src/videogames"+"/"+var1[-1]
        with open(pageurl) as videogamePage:
            return self.__cleanPage(videogamePage)
        
    def __cleanPage(self,page)->str:
        bs4page:object = bs4.BeautifulSoup(page,"html5lib")
        for scriptsAndStyles in bs4page(["script","style","noembed",'noscript']):
            scriptsAndStyles.decompose()
        pageText:str= bs4page.get_text(separator="\n",strip=True)
        return pageText
        
    def createTokens(self,pageText:str)-> list[tuple[any,int]]:
        pageText = re.sub(r"[\|:!-,]|\t+|[^\w](\.)+", '', pageText) #remove annoying charachters 
        # tokentext=word_tokenize(pageText,preserve_line=True) #tokenize into sentences and then words 
        tokenizedLemmatizedText = [t.lemma_.strip() for t in self.nlp(pageText) ]# tokenizes and lemmatized the Incomming text 
        filteredTokens = [ word for word in tokenizedLemmatizedText if word.lower() not in stopwords.words('english') and len(word)>1] #filter to remove stopwords and insignificant charachters 
        # bigrams = nltk.bigrams(filteredTokens) #find bigrams 
        # bigramsFrequency = nltk.FreqDist(bigrams) # make frequency of bigrams
        indexDict = Counter(filteredTokens) #store frequency of those lemmitized words
        return indexDict
 
# test = Indexer()
# ttext = test.openPage(["videogame/ps2.gamespy.com/zatch-bell.html","Teen","Bandai","Fighting","Eighting"])
# test.createTokens(ttext)
# tokenDictionary{
#     word:{
#         totalDocumentFrequency:int,
#         postings:{
#             documentName:{
#                 occurances:int,
#                 positions:[]
#                             }
#         }
#     }
# }

