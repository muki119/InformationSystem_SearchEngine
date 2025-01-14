import pickle
import os
class InvertedIndex:
    """Inverted Index Data structure Made by Mugagga Kimera"""
    def __init__(self,objectFilePath:str)->None:
        """If given one file path , will attempt to find metadata file from same directory"""
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
        self.filePathDirectory = os.path.dirname(objectFilePath)
        self.__objectFilePath:str = self.filePathDirectory+"/wordIndex.pk1"
        self.__metadataFilePath:str = self.filePathDirectory + "/documentMetadata.pk1"
        self.dictionary = self.__getDictionaryFile() # dictionary where the inverted index is stored
        self.metadata = self.__getMetadataFile() # index of file metadata

    def __len__(self):
        return len(self.dictionary)
    def __getFile(self,filePath:str,isMetadata:bool = False)->dict:
        try:
            with open(filePath,'rb') as fileToRead: # open the file
                print(f'Loaded:{filePath}')
                return pickle.load(fileToRead)
            # if it's not a file but a file path
        except FileNotFoundError: # if file not found
            print(f'File :{filePath} not found ... File will be created on dump')
            self.__createFilePath(filePath)
            return dict()
        except EOFError: # END OF FILE (empty file)
            print("File is empty")
            return dict()
        except Exception as error:
            print('An error has occurred: '+str(error))
            return dict()

    def __createFilePath(self,filePath:str)->dict:
        directory = os.path.dirname(filePath)
        if not os.path.exists(directory): # if the file path dosent exist
            print(f'Directory {directory} does not exist. Creating...')
            os.makedirs(directory) # make the file directory

    def isEmpty(self)->bool:
            return not bool(len(self.dictionary)) #only empty if not built and file dosen't exist

    def __getDictionaryFile(self)->dict: # gets the metadata file from the directory
        return self.__getFile(self.__objectFilePath)
    
    def __getMetadataFile(self)->dict:
        return self.__getFile(self.__metadataFilePath,True)
    
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

