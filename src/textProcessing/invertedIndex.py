import pickle
class InvertedIndex():
    def __init__(self,objectFilePath):
        self.objectFilePath:str = objectFilePath
        self.dictionary:dict = self.__getDictionaryFile()
        
    def __getDictionaryFile(self)->dict:
        try:
            with open(self.objectFilePath,'rb') as fileToRead:
                return pickle.load(fileToRead)
        except FileNotFoundError: # if file not found
            print("File not found , file will be created on dump")
            return {}
        except EOFError: # END OF FILE (empty file)
            print("File is empty")
            return {}
        except Exception as error:
            print('An error has occurred: '+str(error))
    
    def __getitem__(self,key:str)->any:
        return self.dictionary.get(key)
    
    def __setitem__(self,key:str,value:any)->None:
        self.dictionary[key] = value
        
    def dumpDictionary(self)->None:
        try:
            with open(self.objectFilePath,'wb') as fileToWrite: 
                pickle.dump(self.dictionary,fileToWrite)
        except FileNotFoundError:
            print("File Cannot be found:"+self.objectFilePath)
            
    def addWord(self,word:str,documentName:str,occurences:int,positions:list[int])->None:
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
        if word not in self.dictionary: # if word isnt in index - add it to index 
            self.dictionary[word]={
                "totalDocumentFrequency":0,
                "totalOccurrences":0,
                "postings":{}
            }
            
        if documentName not in self[word]['postings']: # if document isnt in word postings - add it 
            self.dictionary[word]['postings'][documentName] = {
                "occurences":occurences,
                "positions":positions
            }  
            self.dictionary[word]['totalDocumentFrequency']+=1
            self.dictionary[word]['totalOccurrences']+=occurences
    
inverted = InvertedIndex("src/what.pk1")

inverted.dumpDictionary()