#replace with current pymongotest.py

from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
from flask_socketio import SocketIO
import bson
import json
import string
import nltk, re, pprint
from nltk import word_tokenize, pos_tag
from nltk.corpus import wordnet as wn
from nltk.stem import PorterStemmer
ps = PorterStemmer()




def symmetric_sentence_similarity(sentence1, sentence2):
    
    return (sentence_similarity(sentence1, sentence2) + sentence_similarity(sentence2, sentence1)) 
def penn_to_wn(tag):
    
    if tag.startswith('N'):
        return 'n'
 
    if tag.startswith('V'):
        return 'v'
 
    if tag.startswith('J'):
        return 'a'
 
    if tag.startswith('R'):
        return 'r'
 
    return None
 
def tagged_to_synset(word, tag):
    wn_tag = penn_to_wn(tag)
    if wn_tag is None:
        return None
 
    try:
        return wn.synsets(word, wn_tag)[0]
    except:
        return None
 
def sentence_similarity(sentence1, sentence2):
    """ compute the sentence similarity using Wordnet """
   
    sentence1 = pos_tag(word_tokenize(sentence1))
    sentence2 = pos_tag(word_tokenize(sentence2))
 
   
    synsets1 = [tagged_to_synset(*tagged_word) for tagged_word in sentence1]
    synsets2 = [tagged_to_synset(*tagged_word) for tagged_word in sentence2]
 
    
    synsets1 = [ss for ss in synsets1 if ss]
    synsets2 = [ss for ss in synsets2 if ss]
 
    score, count = 0.0, 0
 
    
    for synset in synsets1:
        
        best_score = max([synset.path_similarity(ss) for ss in synsets2])
 
        
        if best_score is not None:
            score += best_score
            count += 2
 
    
    if count > 0 :
        score /= count
    return score
 


app = Flask(__name__)

socketio = SocketIO(app)

app.config['MONGO_DBNAME'] = 'testfilesearch'
app.config['MONGO_URI'] = 'mongodb://amith:amith123@ds239368.mlab.com:39368/vor'

mongo = PyMongo(app)

def get_nested(data, *args):
      if args and data:
        element  = args[0]
        if element:
            value = data.get(element)
            return value if len(args) == 1 else get_nested(value, *args[1:]) 


@socketio.on('input')
def get_all_frameworks(name):
    r=''
    for i in '!@#$%^&*()_+-={}[]|\\\';:"<,>.?/':
           r=name.split(i)
           name=' '.join(r)
    name=name.lower()
    name2=name.split()
    n=[]
    f=open('stopwords.txt','r')
    stopword=f.read().split()
    for word in name2:
      if word not in stopword:
         n.append(word)
    name2=n
    stemmed=[ps.stem(w) for w in name2]
    print (name2)
    doc = []
    output = []
    
    
    framework = mongo.db.TFIDFtest

    output1 = []
    f=open('ID.txt','r')
    
    doc=eval(f.read())
   
    x=0
    y=0
    m=0
    l=0
    s=0
    try:
        for q in framework.find():
            output1.append({'files' : q[stemmed[y]]})
        while x < 23:
            
            s=0
            y=0
            flag=True
            while y < len(stemmed):
                
               
                if get_nested(q,stemmed[y],doc[x])==None:
                    flag=False
                    break
                s= s + get_nested(q,stemmed[y],doc[x])
                
                y=y+1
            if s > l and flag:
                
                l=s
                m=x    
            x=x+1
    except:
        print('An error occurred.')
        output1= {"output": {"contents": ['Oops! I am sorry, I am confused']}}
        socketio.emit('output',output1) 
    #return;	
        
    print(doc[m]) 
    
    crawl = mongo.db.testfilesearch
    c = crawl.find_one({'_id' : bson.ObjectId(doc[m])})
     
    if c:
      output1 = {'output' : c['content']}
    else:
      output1 = "No such name"
    
    print(len(output1['output']['contents']))
    b=0
    score=0
    best1=0
    para=0
    while b < len(output1['output']['contents']) :
        mylist = json.dumps(output1['output']['contents'][b])
        if len(mylist) > 10:
            score=symmetric_sentence_similarity(name, mylist)
            if score > best1 :
                best1=score
                para=b
        b+=1
    output2=output1['output']['contents'][para]
    output1= {"output": {"contents": [output2]}}            
    socketio.emit('output',output1)
    return jsonify({'search result' : output})
      





if __name__ == '__main__':
    socketio.run(app)
