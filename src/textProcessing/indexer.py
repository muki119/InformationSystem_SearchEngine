import bs4
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import re
from textProcessing import invertedIndex

lemmatizer = WordNetLemmatizer()
def buildIndex():

    videogamesLine=None
    wordIndex = invertedIndex.InvertedIndex('src/wordIndex.pk1')
    with open('src/videogame-labels.csv') as videogameLabels :
        videogamesLine = videogameLabels.readlines()[1:]#ignore first line which is just formatting  
    for pageLineInfo in videogamesLine: # open each page and create its tokens
        pageData = pageLineInfo.rstrip().split(",")
        pageText:str = openPage(pageData)
        tokenFreqdist:dict = createTokens(pageText)#dictionary of tokens and their frequency
        for token , freq in tokenFreqdist:
            wordIndex.addWord(token,pageData[0],freq,[1,2,4,5,6])
    wordIndex.showDict()
    wordIndex.dumpDictionary()
                
def openPage(pageLineInfo:list[str])->str:
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
        return pageText
    
    
def createTokens(pageText:str):
    pageText = re.sub(r"[\|:!-,]|\t+|[^\w](\.)+", '', pageText) #remove annoying charachters 
    tokentext=word_tokenize(pageText,preserve_line=True) #tokenize into sentences and then words 
    filteredTokens = [word for word in tokentext if word.lower() not in stopwords.words('english') and len(word)>1] #filter to remove stopwords and insignificant charachters 
    # bigrams = nltk.bigrams(filteredTokens) #find bigrams 
    # bigramsFrequency = nltk.FreqDist(bigrams) # make frequency of bigrams
    
    lemWords = [lemmatizer.lemmatize(lems) for lems in filteredTokens] #lemmitize 
    indexDict = nltk.FreqDist(lemWords) #store frequency of those lemmitized words
    return indexDict.most_common(30)
 
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

buildIndex()

