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

@app.route('/crawl/<name>', methods=['GET'])
def get_all_frameworks(name):
    framework = mongo.db.TFIDF

    output = []

    for q in framework.find():
        output.append({'files' : q[name]})

    return jsonify({'result' : output})


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
