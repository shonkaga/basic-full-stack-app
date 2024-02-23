###################################################
# Starting and linking Flask together with SQL
###################################################
#importing what we need 
import os
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

# creating an instance of a flask application.
app = Flask(__name__)

#find the directory we are currently in
dir_path = os.path.dirname(os.path.realpath(__file__))

# Connects our Flask App to our Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(dir_path, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#starts our data base
db = SQLAlchemy(app)
###################################################


####################################################
# Create a user table and start the Database
class User(db.Model):
  # columns:
  id = db.Column(db.Integer,primary_key=True)
  username= db.Column(db.Text)
  name= db.Column(db.Text)

  def __init__(self,username,name):
    self.username = username
    self.name = name
  
  def __repr__(self):
    return (f"USERNAME: {self.username}      NAME:{self.name}")


######################################################
#home page
@app.route('/')
def index():
  userList = User.query.all()
  return render_template('index.html',userList=userList)

#add page
@app.route('/add')
def add():
  return render_template('add.html')

#added page
@app.route('/added')
def added():
  username = request.args.get('username')
  name = request.args.get('name')

  newUser = User(username,name)
  db.session.add(newUser)
  db.session.commit()

  message = f"We have added a new user: {username} "
  userList = User.query.all()
  return render_template('index.html',userList=userList,message=message)

# delete page
@app.route('/delete')
def delete():
  userList = User.query.all()
  return render_template('delete.html', userList=userList)

#deleted page
@app.route('/deleted')
def deleted():
  #FLASK AND FORMS
  userID = request.args.get('userID')

  #SQL
  user = User.query.get(userID)
  username = user.username
  db.session.delete(user)
  db.session.commit()

  #FLASK AND JINJA TEMPLATES
  message = f"We have deleted a user: {username} "
  userList = User.query.all()
  return render_template('index.html',userList=userList,message=message)

#Update Page
@app.route('/update')
def update():
  userList = User.query.all()
  return render_template('update.html', userList=userList)

#updated page
@app.route('/updated')
def updated():
  #FLASK AND FORMS
  userID = request.args.get('userID')
  newUsername = request.args.get('username')
  newName = request.args.get('name')

  #SQL
  user = User.query.get(userID)
  user.username = newUsername
  user.name = newName

  db.session.add(user)
  db.session.commit()

  #FLASK AND JINJA TEMPLATES
  message = f"We have updated the user: {user.username} "
  userList = User.query.all()
  return render_template('index.html',userList=userList,message=message)

# Search route 
@app.route('/search')
def search():
  return render_template('search.html')

#searched
@app.route('/searched')
def searched():
  userID = request.args.get('userID')
  user = User.query.get(userID)

  print(f"User ID: {userID}")
  print(f"User : {user}")



  if(user):
    message = f"The user has an id: {userID} and a username of {user.username}"
  else:
    message = "This user does not exist"


  return render_template('search.html',message=message)


if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')
    # fuly start the Tables
    db.create_all()
