# -*- coding: utf-8 -*-
"""
Created on Tue Feb 20 12:24:33 2018

@author: C63165
"""
import json
from Indexer import Document
from Indexer import getURL
from Indexer import openURL

class Doc(Document):
    """
    A class which represents a document. Inherits from the original Document class in Indexer.py
    """
    def __init__(self,js):
        """
        input:
            js- a dictionary which corresponds to a document. This is obtained from the processed json.
        output:
            initializes a Document object.
        """
        Document.__init__(self,js)
        self.title=js["content"]["title"]
        self.title=self.title.lower().split()
        
class Docs(object):
    """
    A class which represents a collection of documents. 
    Reads directly from the processed json file and TFIDF json file to create documents and add to collection.
    """
    def __init__(self,processed,TFIDF):
        """
        Initializes a Docs object.
        Input:
            processed- file name of the processed json file (string).
            TFIDF- file name of the TFIDF json file (string).
        Output:
            Initializes a Docs object directly from the resulting files of importData() in ImportData.py
        """
        file=open(processed,'r',encoding='utf8')
        jsonstr=file.read()
        self.ddict=json.loads(jsonstr)
        file.close()
        
        file=open(TFIDF,'r',encoding='utf8')
        jsonstr=file.read()
        self.TFIDF=json.loads(jsonstr)
        file.close()
        
        self.docs=[]
        for d in self.ddict:
            try: 
              doc=Doc(self.ddict[d])
              self.docs.append(doc)
            except:
              continue
        self.exportDocID()
    def getMatch(self,words):
        """
        Returns the ID of the document which corresponds to the best match for the list of words.
        input:
            words- a list of words.
        """
        best=0
        bestmatch=None
        for doc in self.docs:
            s=0
            flag=True
            for word in words:
                if word not in doc.getWordList():
                    flag=False
                    break
                s=s+self.TFIDF[word][doc.getID()]
            if s>best and flag:
                bestmatch=doc.getID()
                best=s
        return bestmatch
    
    def openPage(self,words):
        """
        Opens the webpage corresponding to the best match of the given words.
        input:
            words- a list of words.
        """
        openURL(getURL(self.ddict,self.getMatch(words)))
        
    def getDocID(self):
        """
        Returns a list of IDs of all the documents in the collection.
        """
        ID=[]
        for doc in self.docs:
            ID.append(doc.getID())
        return ID
    
    def exportDocID(self):
        """
        Exports the list of Document IDs and stores it in a text file.
        """
        ID=open('ID.txt','w',encoding='utf8')
        ID.write(str(self.getDocID()))
        ID.close()
    
    
docs=Docs('processed.json','TFIDF.json')

