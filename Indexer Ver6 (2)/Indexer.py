# -*- coding: utf-8 -*-
"""
Created on Fri Feb 16 16:45:29 2018

@author: C63165
"""

import json
import math
import webbrowser             
def processJSON(dest,files,overwrite=True):
    """
    Processed the JSON file which was exported from mongoDB and returns a valid JSON file.
    Inputs:
        dest- Name of the destination file (string)
        files- list of JSON file names which were exported from mongoDB (list)
        overwrite- whether or not the destination file should be overwritten. (boolean)
    Outputs:
        writes a JSON file with the name dest
        returns a python dictionary corresponding to the JSON file
    """
    rawlist=[]
    for file in files:
     crawl=open(file,'r',encoding='utf8')
     rawdata=crawl.read()
     crawl.close()
     curlycount=0
     chunk=''
     for letter in rawdata:
       chunk=str(chunk)+letter
       if letter=='{':
        curlycount+=1
       if letter=='}':
        curlycount-=1
       if curlycount==0 and len(chunk)==1:
           chunk=''
       elif curlycount==0 and len(chunk)>1:
        rawlist.append(chunk)
        chunk=''
        
    start=0  
    js1='{}'
    if not overwrite:
      file1=open(dest,'r',encoding='utf8')
      js1=file1.read()
      file1.close()
      js2=json.loads(js1)
      start=max([int(i[1:]) for i in js2])+1
      js1=js1[:-1]+','+'}'
    
    js='{'
    for i in range(len(rawlist)):
     js=js+'"d'+str(i+start)+'":'+rawlist[i]+','
    js=js[:-1]+'}' 
    
    jsf=js1[:-1]+js[1:]
    file1=open(dest,'w',encoding='utf8')
    file1.write(jsf)
    file1.close()
    return json.loads(jsf)

class Document(object):
    """
    A class which represents an individual document.
    """
    def __init__(self,js):
        """
        input:
            js- a dictionary which corresponds to a document. This is obtained from the processed json.
        output:
            initializes a Document object.
        """
        self.ID=js["_id"]["$oid"]
        self.stringlist=js["content"]["contents"]
        self.string=' '.join(self.stringlist)
        r=''
        for i in '!@#$%^&*()_+-={}[]|\\\';:"<,>.?/':
           r=self.string.split(i)
           self.string=' '.join(r)
        self.string=self.string.lower()
        self.wordlist=self.string.split()
#        self.TF={}
#        self.computeTF()
    
    def getWordCount(self):
        """
        returns the word count of the document (excluding the stop words).
        """
        return len(self.wordlist)
    
    def getWordList(self):
        """
        returns a list containing the words in the document (excluding the stop words).
        """
        return self.wordlist
    
    def getCountOf(self,word):
        """
        returns the number of occurances of the word in the document.
        """
        return self.wordlist.count(word)
    
    def isWordIn(self,word):
        """
        returns True if the word is in document, False otherwise.
        """
        return word in self.wordlist
    
    def getTF(self,word):
        """
        returns the term frequency (TF) of the word in the document.
        """
        return float(self.getCountOf(word))/float(self.getWordCount())
    
#    def computeTF(self):
#        for word in self.wordlist:
#            self.TF[word]=self.getTF(word)
    
    def getID(self):
        """
        returns the ID of the document (which is the object id of the document in mongoDB).
        """
        return self.ID
    
    def __eq__(self,doc):
        """
        condition for checking equivalence of two documents.
        Two documents are equal if their ID's are the same.
        """
        return self.ID==doc.ID
    
class Documents(object):
    """
    A class which represents a collection of Documents.
    """
    def __init__(self):
        """
        Initializes a Documents object.
        """
        self.docs=[]
        self.wordlist=[]
        self.IDF={}
        self.TFIDF={}
#        self.word_doc={}
        stopfile=open('stopwords.txt','r',encoding='utf8')
        self.stopwords=stopfile.read()
        self.stopwords=self.stopwords.split()
    
    def getNumDocs(self):
        """
        returns the number of documents in the collection.
        """
        return len(self.docs)
    
    def getIDF(self,word):
        """
        Computes the Inverse Document Frequency(IDF) of the word in the collection.
        """
        n=0
        for doc in self.docs:
            if doc.isWordIn(word):
                n=n+1
        return math.log(self.getNumDocs()/n)
    
    def updateIDF(self):
        """
        Computes the IDF of all of the words in the wordlist of the collection and stores the values in self.IDF (a dictionary).
        """
        for word in self.wordlist:
            self.IDF[word]=self.getIDF(word)
    
    def computeTFIDF(self):
        """
        Computes the TFIDF of all the words for each of the document in the collection and stores the values in self.TFIDF (a dictionary of dictionaries).
        """
        for word in self.wordlist:
            for doc in self.docs:
                if word in doc.wordlist:
                     self.TFIDF[word][doc.getID()]=doc.getTF(word)*self.IDF[word]
#                else:
#                    self.TFIDF[word][doc.getID()]=0
            
    def addDoc(self,doc):
        """
        Adds a document to the collection and updates the wordlist.
        input:
            doc- a Document object.
        """
        if doc not in self.docs:
            self.docs.append(doc)
            for word in doc.getWordList():
                if  word not in self.wordlist:
                    if len(word)>1 and word not in self.stopwords:
                      self.wordlist.append(word)

    def getMatch(self, words):
        """
        Returns the ID of the document which corresponds to the best match for the list of words
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
    
    def update(self):
        """
        Updates self.IDF and self.TFIDF
        """
        print('Initializing Indexing...')
        for word in self.wordlist:
          self.TFIDF[word]={}
        print('Initializing Done!')
        print('Computing IDF...')
        self.updateIDF()
        print('Computing IDF done!')
        print('Computing TFIDF...')
        self.computeTFIDF()
        print('Computing TFIDF Done!')
        print('Finished Updating!')
    
    def exportToCSV(self):
        """
        Exports the TFIDF data to a csv file.
        """
        print('Exporting to TFIDF.csv...')
        file=open('TFIDF.csv','w',encoding='utf8')
        file.write('Word,')
        for doc in self.docs:
            file.write(doc.getID()+',')
        file.write('\n')
        for word in self.wordlist:
            file.write(word+',')
            for doc in self.docs:
              if word in doc.getWordList():
                file.write(str(self.TFIDF[word][doc.getID()])+',')
              else:
                 file.write(str(0)+',') 
            file.write('\n')
        file.close()
        print('Exporting Done!')
    
    def exportToJSON(self):
        """
        Exports the TFIDF data to a json file.
        """
        print('Exporting to TFIDF.json...')
        jsonstr=json.dumps(self.TFIDF)
        file=open('TFIDF.json','w',encoding='utf8')
        file.write(jsonstr)
        file.close
        print('Exporting Done!')
             
def getURL(ddict,ID):
    """
    Returns the url of the document corresponding to the given document ID.
    input:
        ddict- The dictionary which was returned from processJSON().
        ID- Document ID (string).
    output:
        url- the url of the document (string).
    """
    for d in ddict:
        if ddict[d]["_id"]["$oid"]==ID:
            url="https://en.wikipedia.org"+ ddict[d]['title']
            return url
    return None

def openURL(url):
  """
  Opens the url in the default webpage.
  input:
      url- the url to be opened (string).
  """
  try:
    webbrowser.open_new(url)
  except:
      print('Could not open webpage: no match found!')

def openPage(ddict,docs,words):
    """
    Opens the webpage corresponding to the keywords.
    inputs:
        ddict: The dictionary which was returned from processJSON().
        docs: a Documents object.
        words: a list of words.
    """
    openURL(getURL(ddict,docs.getMatch(words)))

def getPara(ddict,docs,words,n):
    """
    Returns the nth paragraph from the document corresponding to the best match for the given words.
    input:
        ddict:The dictionary which was returned from processJSON().
        docs: a Documents object.
        words: a list of words.
        n: paragraph number(int).
    output:
        nth paragraph (string).
    """
    ID=docs.getMatch(words)
    for d in ddict:
        if ddict[d]["_id"]["$oid"]==ID:
            intro=ddict[d]['content']['contents'][n]
            return intro
    return None

def getIntro(ddict,docs,words):
    """
    Returns the 1st paragraph from the document corresponding to the best match for the given words.
    input:
        ddict:The dictionary which was returned from processJSON().
        docs: a Documents object.
        words: a list of words.
    output:
        first paragraph (string).
    """
    return getPara(ddict,docs,words,0)
        
    
