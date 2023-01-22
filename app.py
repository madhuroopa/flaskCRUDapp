from pymongo import MongoClient
from flask import Flask
from flask_pymongo import PyMongo
from bson.json_util import dumps
from bson.objectid import ObjectId ## library used to generate random strings for id
from flask import jsonify, request  ## convert bson to json
from werkzeug.security import generate_password_hash,check_password_hash

##initializing the flask app
app = Flask(__name__)
## setting a secretkey
app.secret_key="secretkey"

client = MongoClient('localhost', 27017)

db = client.Users
collection = db.user


@app.route('/add',methods=['POST'])

def add_user():
    _json=request.json
    _name=_json['name']
    _email=_json['email']
    _password=_json['pwd']
    if _name and _email and _password and request.method=='POST':
        _hashed_password = generate_password_hash(_password)
        id = collection.insert_one({'name':_name,'email':_email,'pwd':_hashed_password})
        res = jsonify("User added successfully")
        res.status_code=200
        return res
    else:
        return not_found()
@app.route('/users')
def users():
    users = collection.find()
    resp=dumps(users)
    return resp
@app.route('/user/<id>')
def user(id):
    user = collection.find_one({'_id':ObjectId(id)})
    resp=dumps(user)
    return resp
@app.route('/delete/<id>',methods=['DELETE'])
def delete_user(id):
    collection.delete_one({'_id':ObjectId(id)})
    resp=jsonify("User deleted successfully")
    resp.status_code=200
    return resp
@app.route('/update/<id>',methods=['PUT'])
def update_user(id):
    _id=id
    _json=request.json
    _name=_json['name']
    _email=_json['email']
    _pwd=_json['pwd']
    if _name and _email and _pwd and _id and request.method=='PUT':
      _hashed_password = generate_password_hash(_pwd)
      collection.update_one({'_id': ObjectId(_id['$oid']) if '$oid' in _id else ObjectId(_id)},
                               {'$set': {'name': _name, 'email': _email, 'password:': _hashed_password}})
      resp = jsonify("User updated successfully")
      resp.status_code = 200

      return resp
    else:

        return not_found()


@app.errorhandler(404)
def not_found(error=None):
    message = {
        'status':404,
        'message':'Not Found'+request.url
    }
    resp = jsonify(message)
    resp.status_code=404
    return resp


if __name__ == "__main__":
    app.run(debug=True)  ## for running the app and debug = true means, the app gets restsrted when we make any changes
