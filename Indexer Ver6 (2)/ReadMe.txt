Description of files:
1) crawleq.json - JSON file which was exported from mongoDB. Update name in ImportData.py if changed.
2) stopwords.txt - Text file containing stop words. Update this file as and when required. Used in Indexer.py
3) Indexer.py - python file containing most of the important classes, methods and functions
4) ImportData.py - python file used to import documents
5) Search.py - python file which reads directly from the resulting files from ImportData.py and can be used to search keywords
6) processed.json- JSON file which gets created as result of processJSON() in Indexer.py
7) TFIDF.csv - CSV file which stores the TFIDF data. Created from ImportData.py
8) TFIDF.json - JSON file which stores the TFIDF data. Created from ImportData.py, and used to import TFIDF data to mongoDB.
9) ID.txt - Text file containing the list of document IDs. Generated from Search.py

Instructions:
1) Run ImportData.py to import data.
2) Run Search.py for carrying out search.

Note:
1) The python files read and write a lot of files. So if the names or the number of any of these files are changed, update the same in the python code as well. 
2) All the code is in python 3.6