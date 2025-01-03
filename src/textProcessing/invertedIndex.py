import pickle
class InvertedIndex():
    """Inverted Index Data structure Made by Mugagga Kimera"""
    def __init__(self,objectFilePath:str)->None:
        """ tokenDictionary{
            word:{
                totalDocumentFrequency:int,
                postings:{
                    documentName:{
                        occurances:int,
                        positions:[]
                    }
                }
            }
        }
        """
        self.__objectFilePath:str = objectFilePath
        self.__metadataFilePath:str = 'src/wordMetadata.pk1'
        self.dictionary = self.__getDictionaryFile()
        self.metadata = self.__getMetadataFile()
    
    def __getFile(self,filePath:str)->dict:
        try:
            with open(filePath,'rb') as fileToRead:
                return pickle.load(fileToRead)
        except FileNotFoundError: # if file not found
            print("File not found , file will be created on dump")
            return dict()
        except EOFError: # END OF FILE (empty file)
            print("File is empty")
            return dict()
        except Exception as error:
            print('An error has occurred: '+str(error))
            return dict()
        
    def __getDictionaryFile(self)->dict:
        return self.__getFile(self.__objectFilePath)
    
    def __getMetadataFile(self)->dict:
        return self.__getFile(self.__metadataFilePath)
    
    def __getitem__(self,key:str)->any:
        return self.dictionary.get(key)
    
    def __setitem__(self,key:str,value:any)->None:
        self.dictionary[key] = value
       
    def getMetadataItem(self,key:str)->any:
        return self.metadata.get(key)
    def getDictionary(self)->dict:
        return self.dictionary
    def getMetadata(self)->dict:
        return self.metadata
    def setMetadataItem(self,key:str,value:any)->None:
        self.metadata[key] = value
         
    def dumpDictionary(self)->None:
        """Saves Dictionary to file specified in object creation.
            Will create the file if it does not exist.
        """
        try:
            with open(self.__objectFilePath,'wb') as fileToWrite: 
                pickle.dump(self.dictionary,fileToWrite)
        except FileNotFoundError:
            print("File Cannot be found:"+self.__objectFilePath)
        except Exception as error:
            print('An error has occurred: '+str(error))
        try:
            with open(self.__metadataFilePath,'wb') as fileToWrite: 
                pickle.dump(self.metadata,fileToWrite)
        except FileNotFoundError:
            print("File Cannot be found:"+self.__metadataFilePath)
        except Exception as error:
            print('An error has occurred: '+str(error))
            
    def addWord(self,word:str,documentName:str,occurrences:int,positions:list[int],metaData:tuple[str])->None:
        """Adds word to inverted index and adds document data to the index. """
        if word not in self.dictionary: # if word isnt in index - add it to index 
            self.dictionary[word]={
                "totalDocumentFrequency":0,
                "totalOccurrences":0,
                "postings":{}
            }

                
        if documentName not in self[word]['postings']: # if document isnt in word postings - add it 
            self.dictionary[word]['postings'][documentName] = {
                "occurrences":occurrences,
                "positions":positions
            }  
            self.dictionary[word]['totalDocumentFrequency']+=1
            self.dictionary[word]['totalOccurrences']+=occurrences 
            
        if documentName not in self.metadata:
                self.metadata[documentName] = {
                    "totalWords":0,
                    "gameInformation":metaData
                }
            
        self.metadata[documentName]['totalWords']+=occurrences   # if document is in word postings - upda
    def displayDictionary(self):
        """Outputs dictionaries contents into file called 'showDictionary.txt'."""
        with open('src/showDictionary.txt','w') as f:
            for words,data in self.dictionary.items():
                f.writelines(f"\n{words}")
                for x , y in data.items():
                    f.writelines(f" \n \tdata:{x} - values:{y}")
