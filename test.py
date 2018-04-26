#!/usr/bin/env python
import tika
import glob
import errno
from tika import parser
path ='./Docs/*.mp3'
files = glob.glob(path)
i=0
for name in files:
    parsed = parser.from_file(name)
    #print(parsed["metadata"])
    print(parsed["content"])
    fh = open(str(i+1)+'.txt',"w")
    fh.write(parsed["content"].encode('utf-8'))
    fh.close()
    i+=1