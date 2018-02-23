from flask import Flask, request
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from json import dumps

db_connect = create_engine('mongodb://amith:amith123@ds239368.mlab.com:39368/vor')
app = Flask(__name__)
api = Api(app)

class Employees(Resource):
    def get(self):
        conn = db_connect.connect()
	query = conn.execute("db.crawl.find().pretty()") # This line performs query and returns json result
        return {'employees': [i[0] for i in query.cursor.fetchall()]}


api.add_resource(Employees, '/employees')


if __name__ == '__main__':
     app.run(port='5002')
