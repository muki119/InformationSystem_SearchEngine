import bs4
import spacy
import concurrent.futures
from collections import Counter
from nltk.corpus import stopwords
import re
from textProcessing import invertedIndex
class Indexer():
    stopwords = set(stopwords.words('english'))
    def __init__(self,path:str):
        self.nlp = spacy.load("en_core_web_sm")
        self.index = invertedIndex.InvertedIndex(path)
        
    def buildIndex(self):#
        try:
            videogamesLine:str=None
            with open('src/videogame-labels.csv') as videogameLabels :
                videogamesLine = videogameLabels.readlines()[1:]#ignore first line which is just formatting  
            print("Reading and Proccessing files...")
            
            with concurrent.futures.ThreadPoolExecutor(max_workers=6) as executor: #multithreading to speed up the process  
                executor.map(self.__processPage,videogamesLine) # tells threads to process the pages in the list
                
            print("Building Index")
            self.index.displayDictionary() #create a output file of the index
            self.index.dumpDictionary() #save the index to a file
            print("Done")
        except Exception as e:
            print("Error While Building Index")
            print(e)
    
    def __processPage(self,pageLineInfo):
        try:
            pageData = pageLineInfo.rstrip().split(",") #split the page meta data
            pageText:str = self.__openPage(pageData) #open the page , clean it and get the text within it 
            tokenFreqdist:dict = self.createTokens(pageText) # create tokens ftom the text and get the frequency of each token ,store in a dictionary.
            for token , freq in tokenFreqdist.items():
                self.index.addWord(token,pageData[0],freq,[1,2,4,5,6]) #add the token data to the index.
        except Exception as e:
            print("Error While Processing Page")
            print(e)

       
        
    def __openPage(self,pageLineInfo:list[str])->str:
        # url,STRING : esrb,STRING : publisher,STRING : genre,STRING : developer
        print("Opening Page: "+pageLineInfo[0],end="\r",flush=True)
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
        
    def createTokens(self,pageText:str)-> dict:
        pageText = re.sub(r"[\|:!-,]|\t+|[^\w](\.)+", '', pageText) #remove annoying charachters 
        tokenizedLemmatizedText = [t.lemma_.strip() for t in self.nlp(pageText,disable=["textcat","ner"],) ]# tokenizes and lemmatized the Incomming text 
        filteredTokens = [ word for word in tokenizedLemmatizedText if word.lower() not in self.stopwords and len(word)>1] #filter to remove stopwords and insignificant charachters 
        # bigrams = nltk.bigrams(filteredTokens) #find bigrams 
        # bigramsFrequency = nltk.FreqDist(bigrams) # make frequency of bigrams
        indexDict = Counter(filteredTokens) #store frequency of those lemmitized words
        return indexDict
 
# test = Indexer('src/wordIndex.pk1')
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

