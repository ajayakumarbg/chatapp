# -*- coding: utf-8 -*-
"""
Created on Fri Feb 16 16:07:45 2018

@author: C63165
"""
from Indexer import Document
from Indexer import Documents
from Indexer import processJSON
import time

t0=time.time()
print('Initiallizing import...')
docs=Documents()
ddict=processJSON('crawl2.json')
i=1
for d in ddict:
   try: 
    doc=Document(ddict[d])
    print('Importing Document No: '+str(i)+'...')
    docs.addDoc(doc)
    i+=1
   except:
       continue
print('Importing Done!')
docs.update()
docs.exportToCSV()
docs.exportToJSON()
t1=time.time()
print('Time Taken: '+str(t1-t0))
t1=time.time()
print('Time taken: '+str(t1-t0))   