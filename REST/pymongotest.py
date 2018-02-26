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
    framework = mongo.db.TFIDF

    output = []
    doc=["5a8fd4500262df2da409af79","5a8fd4540262df2da409af7a","5a8fd4560262df2da409af7b","5a8fd4590262df2da409af7c","5a8fd45c0262df2da409af7d","5a8fd4600262df2da409af7e","5a8fd4620262df2da409af7f","5a8fd4660262df2da409af80","5a8fd4680262df2da409af81","5a8fd46b0262df2da409af82","5a8fd46e0262df2da409af83","5a8fd4710262df2da409af84","5a8fd4730262df2da409af85","5a8fd4760262df2da409af86","5a8fd4790262df2da409af87","5a8fd47c0262df2da409af88","5a8fd4800262df2da409af89"] 
        

    for q in framework.find():
        output.append({'files' : q[name]})
    print(type(output))
    x=0
    m=0
    l=get_nested(q,name,doc[0])
    while x < 17:
        score=get_nested(q,name,doc[x])
        if score > l:
            l= get_nested(q,name,doc[x])
            m=x
        #print(score)
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
