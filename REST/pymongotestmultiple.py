from flask import Flask, jsonify, request
from flask.ext.pymongo import PyMongo
import bson
#from pymongo.objectid import ObjectId
#from flask_restful import Resource, Api

app = Flask(__name__)
#api = Api(app)

app.config['MONGO_DBNAME'] = 'crawl'
app.config['MONGO_URI'] = 'mongodb://amith:amith123@ds239368.mlab.com:39368/vor'

mongo = PyMongo(app)
#def takeSecond(elem):
    #return elem[]
def get_nested(data, *args):
      if args and data:
        element  = args[0]
        if element:
            value = data.get(element)
            return value if len(args) == 1 else get_nested(value, *args[1:]) 


@app.route('/crawl/<name>', methods=['GET'])
def get_all_frameworks(name):
    name2=name.split(",")
    print name2[0]
    doc = []
    #i = 0 
    #for itm in mongo.db.crawl.find():
       #k=itm['_id']
       #k=str(k)
       #doc[i]= "k"
       #doc[1]=k
       #print(k)
       #i=i+1
    #print(k)
    #z=0
    #doc = []
    #ls =  mongo.db.crawl
    #lst =[]
    #for ln in ls.find():
      #lst.append({'_id' : ln['_id']})
      #print(lst)
      #z=z+1
      
    #print(lst[1])
    
    framework = mongo.db.TFIDF

    output = []
    f=open('ID.txt','r')
    
    doc=eval(f.read())
    #for q in framework.find():
        #output.append({'files' : q[name]})
    #print(type(output))
    x=0
    y=0
    m=0
    l=0
    s=0
    for q in framework.find():
               output.append({'files' : q[name2[y]]})
    while x < 100:
        
        s=0
        y=0
        flag=True
        while y < len(name2):
            
            #for q in framework.find():
               #output.append({'files' : q[name2[y]]})
            if get_nested(q,name2[y],doc[x])==None:
                 flag=False
                 break
            s= s + get_nested(q,name2[y],doc[x])
            
            y=y+1
        if s > l and flag:
            
            l=s
            m=x    
        x=x+1
    
    #print(doc[m]) 
    #_id = '5a8eabb80262df4a4eec8772'
    #m.decode("hex")
    crawl = mongo.db.crawl
    c = crawl.find_one({'_id' : bson.ObjectId(doc[m])})
     #print(c)
    if c:
      output = {'output' : c['content']}
    else:
      output = "No such name"
    tr = []
    tr= get_nested(q,name)
    #print(tr)
     
    return jsonify({'search result' : output})
      

#@app.route('/crawl/<id>', methods=['GET'])
#def get_one_id(id):
 # find= mongo.db.TFIDF
 # f = find.find_one({id})
#  if f:
  #  output = { 'result' : f['equifax']}
 # return jsonify({'result' : output})
   










#@app.route('/crawl/<id>', methods=['GET'])
#def get_one_id(id):
  #_id = '5a8eabb80262df4a4eec8772'
  #_id.decode("hex")
 # crawl = mongo.db.crawl
  #c = crawl.find_one({'_id' : bson.ObjectId(id)})
  #print(c)
  #if c:
   # output = {'_id' : c['content']}
  #else:
   # output = "No such name"
  #return id
  #return jsonify({'result' : output})


#def matchword_doc(self):
        #for word in self.wordlist:
          #  best=0
           # bestmatch=None
            #for ID in self.TFIDF:
             #   if self.TFIDF[ID][word]>best:
              #      best=self.TFIDF[ID][word]
               #     bestmatch=ID
            #self.word_doc[word]=bestmatch





#api.add_resource(get_all_frameworks, '/crawl')

if __name__ == '__main__':
    app.run(debug=True)
