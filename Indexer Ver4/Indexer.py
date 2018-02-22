# -*- coding: utf-8 -*-
"""
Created on Fri Feb 16 16:45:29 2018

@author: C63165
"""

import json
import math
             
def processJSON(file):
    crawl=open(file,'r')
    rawdata=crawl.read()
    crawl.close()
    rawlist=[]
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
    js='{'
    for i in range(len(rawlist)):
     js=js+'"d'+str(i)+'":'+rawlist[i]+','

    js=js[:-1]+'}'   
    
    file1=open('processed.json','w')
    file1.write(js)
    file1.close()
    return json.loads(js)       

class Document(object):
    def __init__(self,js):
        self.ID=js["_id"]["$oid"]
        self.paralist=js["content"]["contents"]
#        self.string=' '.join(self.stringlist)
        for p in range(len(self.paralist)):
         para=self.paralist[p]
         r=''
         for i in '!@#$%^&*()_+-={}[]|\\\';:"<,>.?/\n':
           r=para.split(i)
           para=' '.join(r)
         self.paralist[p]=para.lower()
        self.string=' '.join(self.paralist)
        self.wordlist=self.string.split()
        stop=open('stop_words.txt','r')
        self.stopwords=stop.read().split()
        stop.close()
        words=[]
        for word in self.wordlist:
            if len(word)>1 and word not in self.stopwords:
                words.append(word)
        self.wordlist=words
        self.Densities={}
        self.updateDensity()
        self.word_para={}
        self.matchword_para()
    
    def getWordCount(self):
        return len(self.wordlist)
    
    def getParalist(self):
        return self.paralist
    
    def getPara(self,n):
        if n<len(self.paralist):
            return self.paralist[n]
        
    def getParaLen(self,n):
        if n<len(self.paralist):
            return len(self.paralist[n].split())
        
    def getParaWordCount(self,word,n):
        if n<len(self.paralist):
            return self.paralist[n].split().count(word)
    
    def getWordDensity(self,word,n):
        if n<len(self.paralist):
            return float(self.getParaWordCount(word,n))/float(self.getParaLen(n))
    
    def updateDensity(self):
        for i in range(len(self.paralist)):
            self.Densities[i]={}
        for i in range(len(self.paralist)):
            for word in self.wordlist:
                if word in self.paralist[i].split():
                    self.Densities[i][word]=self.getWordDensity(word,i)
                else:
                    self.Densities[i][word]=0
                    
    def matchword_para(self):
        for word in self.wordlist:
            best=0
            bestmatch=None
            for i in self.Densities:
                if self.Densities[i][word]>best:
                    best=self.Densities[i][word]
                    bestmatch=i
            self.word_para[word]=bestmatch
            
    def getMatchPara(self,word):
        return (self.word_para[word],self.paralist[self.word_para[word]])
    
    def getWordList(self):
        return self.wordlist
    
    def getCountOf(self,word):
        return self.wordlist.count(word)
    
    def isWordIn(self,word):
        return word in self.wordlist
    
    def getTF(self,word):
        return float(self.getCountOf(word))/float(self.getWordCount())
    
    def getID(self):
        return self.ID
    
    def __eq__(self,doc):
        return self.ID==doc.ID
    
class Documents(object):
    def __init__(self):
        self.docs=[]
        self.wordlist=[]
        self.IDF={}
        self.TFIDF={}
        self.word_doc={}
#        stopfile=open('stop_words.txt','r')
#        self.stopwords=stopfile.read()
#        self.stopwords=self.stopwords.split()
    
    def getNumDocs(self):
        return len(self.docs)
    
    def getIDF(self,word):
        n=0
        for doc in self.docs:
            if doc.isWordIn(word):
                n=n+1
        return math.log(self.getNumDocs()/n)
    
    def updateIDF(self):
        for word in self.wordlist:
            self.IDF[word]=self.getIDF(word)
    
    def computeTFIDF(self):
        for word in self.wordlist:
            for doc in self.docs:
                if word in doc.wordlist:
                     self.TFIDF[doc.getID()][word]=doc.getTF(word)*self.IDF[word]
                else:
                    self.TFIDF[doc.getID()][word]=0
    
    def matchword_doc(self):
        for word in self.wordlist:
            best=0
            bestmatch=None
            for ID in self.TFIDF:
                if self.TFIDF[ID][word]>best:
                    best=self.TFIDF[ID][word]
                    bestmatch=ID
            self.word_doc[word]=bestmatch
            
    def addDoc(self,doc):
        if doc not in self.docs:
            self.docs.append(doc)
            for word in doc.getWordList():
                if  word not in self.wordlist:
#                    if len(word)>1 and word not in self.stopwords:
                      self.wordlist.append(word)

    def getMatch(self, word):
        try:
         return self.word_doc[word]
        except:
            return None
    
    def update(self):
        print('Initializing Indexing...')
        for doc in self.docs:
          self.TFIDF[doc.getID()]={}
        print('Initializing Done!')
        print('Computing IDF...')
        self.updateIDF()
        print('Computing IDF done!')
        print('Computing TFIDF...')
        self.computeTFIDF()
        print('Computing TFIDF Done!')
        self.matchword_doc()
        print('Finished Updating!')
    
    def exportToCSV(self):
        print('Exporting to TFIDF.csv...')
        file=open('TFIDF.csv','w')
        file.write('File ID,')
        for word in self.wordlist:
            file.write(word+',')
        file.write('\n')
        for doc in self.docs:
            file.write(str(doc.getID())+',')
            for word in self.wordlist:
                file.write(str(self.TFIDF[doc.getID()][word])+',')
            file.write('\n')
        file.close()
        print('Exporting Done!')
    
    def exportToJSON(self):
        print('Exporting to TFIDF.json...')
        jsonstr=json.dumps(self.TFIDF)
        file=open('TFIDF.json','w')
        file.write(jsonstr)
        file.close
        print('Exporting Done!')

#ddict=processJSON('crawl.json')