import bs4
import pickle
import numpy
import nltk
from nltk.tokenize import sent_tokenize , word_tokenize,wordpunct_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import re
import string
import pickle

lemmatizer =WordNetLemmatizer()
def indexer():
    try:
        videogamesLine=None
        with open('src/videogame-labels.csv') as videogameLabels :
            videogamesLine = videogameLabels.readlines()[1:]#ignore first line which is just formatting  
        for pageLineInfo in videogamesLine:
            openPage(pageLineInfo.rstrip().split(","))
    except Exception as error:
        print(error)


def openPage(pageLineInfo:list[str]):
    #page line info 
    # url,STRING : esrb,STRING : publisher,STRING : genre,STRING : developer
    #print(pageLineInfo)
    var1  = pageLineInfo[0].split("/")
    pageurl = "src/videogames"+"/"+var1[-1]
    with open(pageurl) as videogamePage:
        bs4page:object = bs4.BeautifulSoup(videogamePage,"html5lib")
        for scriptsAndStyles in bs4page(["script","style","noembed",'noscript']):
            scriptsAndStyles.decompose()
        pageText:str= bs4page.get_text(separator="\n",strip=True)
        createTokens(pageText)
    
    
def createTokens(pageText:str):
    pageText = re.sub(r"[\|:!-,]|\t+|[^\w](\.)+", '', pageText) #remove annoying charachters 
    tokentext=word_tokenize(pageText,preserve_line=True) #tokenize into sentences and then words 
    filteredTokens = [word for word in tokentext if word.lower() not in stopwords.words('english') and len(word)>1] #filter to remove stopwords and insignificant charachters 
    bigrams = nltk.bigrams(filteredTokens) #find bigrams 
    bigramsFrequency = nltk.FreqDist(bigrams) # make frequency of bigrams
    
    lemWords = [lemmatizer.lemmatize(lems) for lems in filteredTokens] #lemmitize 
    indexDict = nltk.FreqDist(lemWords) #store frequency of those lemmitized words
    for key , values in indexDict.most_common(10):
        print(key,values)
 


    return

openPage(["videogame/ps2.gamespy.com/zatch-bell.html","Teen","Bandai","Fighting","Eighting"])

