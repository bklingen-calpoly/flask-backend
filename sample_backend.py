from flask import Flask
from flask import request
from flask import jsonify
import json
# for linking frontend-backend
from flask_cors import CORS

# for random ids 
# import random 
# import string

# for mongo db
from model_mongodb import User


app = Flask(__name__)
#CORS stands for Cross Origin Requests.
#Here we'll allow requests coming from any domain. Not recommended for production environment.
CORS(app) 

users = { 
   'users_list' :
   [
      { 
         'id' : 'xyz789',
         'name' : 'Charlie',
         'job': 'Janitor',
      },
      {
         'id' : 'abc123', 
         'name': 'Mac',
         'job': 'Bouncer',
      },
      {
         'id' : 'ppp222', 
         'name': 'Mac',
         'job': 'Professor',
      }, 
      {
         'id' : 'yat999', 
         'name': 'Dee',
         'job': 'Aspring actress',
      },
      {
         'id' : 'zap555', 
         'name': 'Dennis',
         'job': 'Bartender',
      }
   ]
}

@app.route('/')

def hello_world():
    return 'Hello, World!'
    
# def gen_random_id():
#   random_id = ''.join([random.choice(string.ascii_letters 
#            + string.digits) for n in range(6)]) 
#   print (random_id)
#   return random_id


@app.route('/users', methods=['GET', 'POST'])
def get_users():
   if request.method == 'GET':
      search_username = request.args.get('name')
      print(f'search username {search_username}')
      search_job = request.args.get('job')
      if search_username and search_job :
         users = User().find_by_name_and_job(search_username, search_job)  
      elif search_username  :
         print(f'search username {search_username} db: {User().find_by_name(search_username)}')
         users = User().find_by_name(search_username)
      elif search_job  :
         users = User().find_by_job(search_job)
      else:
         users = User().find_all()
      return {"users_list": users}
   elif request.method == 'POST':
      userToAdd = request.get_json()
      # make DB request to add user
      newUser = User(userToAdd)
      newUser.save()
      resp = jsonify(newUser), 201
      return resp
      
@app.route('/users/<id>', methods=['GET','DELETE'])

def get_user(id):
   if request.method == 'GET':
      user = User({"_id":id})
      if user.reload() :
         return user
      else :
         return jsonify({"error": "User not found"}), 404
   elif request.method == 'DELETE':
      user = User({"_id":id})
      resp = user.remove()
      if (resp['n'] == 1) :
         return {}, 204
      else:
         return jsonify({"error": "User not found"}), 404
