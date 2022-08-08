from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_swagger_ui import get_swaggerui_blueprint
import json
import datetime

app = Flask(__name__)

# .....swagger conf.....#
SWAGGER_URL = '/api/docs'  # URL for exposing Swagger UI (without trailing '/')
API_URL = '/static/swagger.json'  # Our API url (can of course be a local resource)
SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Book Management API"
    }
)
app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)


#...for authentication...
login_manager = LoginManager()

# ....getting data from config.json file.... #
with open('config.json','r') as config:
    fConfig= json.load(config)

#...App URL config...
assert isinstance(fConfig["BASE_URL"], str)
assert  "http" in fConfig['BASE_URL']
BASE_URL = fConfig["BASE_URL"]

# secret App key config
SECRET_KEY = fConfig.get('SECRET_KEY')
assert isinstance(SECRET_KEY, str)
assert SECRET_KEY != ""
app.secret_key = SECRET_KEY

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# setting DB URI
DB_URI = fConfig['PARAMS']['DB_URI']
assert isinstance(DB_URI, str)
assert DB_URI != ""
app.config['SQLALCHEMY_DATABASE_URI']= DB_URI

db=SQLAlchemy(app)
login_manager.init_app(app)


class User(db.Model):
    """An admin user capable of viewing reports/table's data"""

    __tablename__ = 'user'

    email = db.Column(db.String, primary_key=True, unique=True)
    username = db.Column(db.String)
    image = db.Column(db.String)
    password = db.Column(db.String)
    authenticated = db.Column(db.Boolean, default=False)

    @property
    def serialize(self):
       """Return object data in easily serializable format"""
       return {
           'email': self.email,
           'username': self.username,
           'image': self.image,
           'password': self.password,
           'authenticated': self.authenticated,
       }

    def is_active(self):
        """True, as all users are active."""
        return True

    def get_id(self):
        """Return the email address to satisfy Flask-Login's requirements."""
        return self.email

    def is_authenticated(self):
        """Return True if the user is authenticated."""
        return self.authenticated

    def is_anonymous(self):
        """False, as anonymous users aren't supported."""
        return False


class Publication(db.Model):
    """
      MODEL: model class for book publications
    """

    __tablename__= 'publication'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(300), nullable=False)
    priority = db.Column(db.String(20), nullable=False)
    created_at = db.Column(db.String(100), nullable=False)
    updated_at = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(50), nullable=False)
    user = db.Column(db.String(30), nullable=False)
    def __init__(self, title, description, priority, created_at, status, updated_at, user):
        self.title= title
        self.description= description
        self.priority= priority
        self.created_at= created_at
        self.status= status
        self.updated_at= updated_at
        self.user= user

    @property
    def serialize(self):
       """Return object data in easily serializable format"""
       return {
           'id': self.id,
           'title': self.title,
           'description': self.description,
           'priority': self.priority,
           'created_at': self.created_at,
           'status': self.status,
           'user': self.user,
           'updated_at': self.updated_at,
           'time_since_published': self.life()
       }

    def life(self):
         """Generates time elapsed by taking created date as refernce"""
         t1 = datetime.datetime.strptime(self.created_at, '%Y-%m-%d %H:%M:%S.%f')
         t2 = datetime.datetime.now()
         self.time_diff = t2 - t1
         self.time_diff_sec = self.time_diff.total_seconds()
         return str(datetime.timedelta(seconds = self.time_diff_sec))


db.create_all()


@app.route('/', methods=['GET'])
def index():
  """Homepage url handler"""

  return jsonify({'status':200, 'message':'BookAPI is running!!'})


 #...............for books CRUD operations ................ #

@app.route('/addbook', methods=['GET','POST'])
@login_required
def addBook():
  """
        POST: Adds book records in Publications after all checks
        GET:  returns 404 status code/message
  """
  if request.method=='POST':
      data = request.get_json()
      testBook = Publication.query.filter_by(title=data.get('title')).filter_by(description=data.get('description')).first()
      if testBook is not None:
          return jsonify({'status':404, 'message':'This book already exist!!'})
      book = Publication(
          title = data.get('title'),
          description = data.get('description'),
          priority = data.get('priority'),
          user = current_user.email,
          status = data.get('status'),
          created_at = datetime.datetime.now(),
          updated_at = datetime.datetime.now()
      )
      db.session.add(book)
      db.session.commit()
      return jsonify({'status':200, 'message':'your book is added!!'})
  else:
      return jsonify({'status':404, 'message':'wrong request method!!'}),404


@app.route('/updatebook/<id>', methods= ['PUT'])
@login_required
def updatebook(id):
  """
    PUT: Updates book records in Publications after all checks
    param {id}: id of the target book
    return: 404 on error/200 on successful update
  """
  if request.method=='PUT':
      data = request.get_json()
      book = Publication.query.get(id)
      if book is not None:
          if current_user.email == book.user:
              book.title = data.get('title')
              book.description = data.get('description')
              book.priority = data.get('priority')
              book.status = data.get('status')
              book.updated_at = datetime.datetime.now()
              db.session.add(book)
              db.session.commit()
              return jsonify({'status':200, 'message':'your book is Updated!!'})
          else:
              return jsonify({'status':404, 'message':'permission denied!!'}),404
      else:
            return jsonify({'status':404, 'message':'book does not exist!!'}),404
  else:
      return jsonify({'status':404, 'message':'wrong request method!!'}),404


@app.route('/getbook/<id>', methods=['GET'])
@login_required
def getBook(id):
      """
        GET: fetch book by id from db
        param {id}: id of the target book
        return: 404 on error/200 on successful fetch
      """
      book = Publication.query.get(id)
      if book is not None:
          if current_user.email == book.user:
               return jsonify(book.serialize)
          else:
               return jsonify({'status':404, 'message':'permission denied, you can only fetch book(s) created by you!!'}),404
      else:
            return jsonify({'status':404, 'message':'book does not exist!!'}),404


@app.route('/deletebook/<id>', methods=['DELETE'])
@login_required
def deleteBook(id):
      """
        DELETE: delete book by id from db
        param {id}: id of the target book
        return: 404 on error/200 on successful delete
      """
      book = Publication.query.get(id)
      if book is not None:
          if current_user.email == book.user:
               Publication.query.filter_by(id=id).delete()
               db.session.commit()
               return jsonify({'status':200, 'message':'book is deleted!!'})
          else:
               return jsonify({'status':404, 'message':'permission denied!!'}),404
      else:
            return jsonify({'status':404, 'message':'book does not exist!!'}),404



 #...............for user CRUD operations ................ #

@app.route('/signup', methods=['GET','POST'])
def signUp():
      """
        GET: return 404 and error message
        POST: allow user to login after credential validation
        return: 404 on error/200 on successful login
      """
      if request.method == "POST":
            data = request.get_json()
            # print(data)
            email = data.get('email')
            eStatus = User.query.get(email)
            if eStatus is not None:
                return jsonify({'status':404, 'message':'email already registered!!'})
            if data.get('image') is not None:
                image = data.get('image')
                filepath = image.filename
                image.save(f"./static/uploads/images/{filepath}")
            else:
                filepath = 'default.jpg'
            newUser = User(
                         email= email,
                         username= data.get('username'),
                         image= filepath,
                         password= data.get('password'),
                         authenticated= False,
                        )
            db.session.add(newUser)
            db.session.commit()
            return jsonify({'status':200, 'message':'new user created!!'})

      else:
           return jsonify({'status':404, 'message':'wrong request method!!'})


@app.route('/update-user-info', methods=['PUT'])
@login_required
def updateUser():
    """
      PUT: update current logged-in user info
      return: error status/200 on successful update
    """
    if request.method == "PUT":
        user = User.query.filter_by(email= current_user.email).first()
        data = request.get_json()
        if data.get('email') is not None:
            testUser = User.query.get(data.get('email'))
            if testUser is None:
                user.email= data.get('email')
            else:
                return jsonify({'status':500, "message":"Email-id already exist!!"})
        if data.get('username') is not None:
            user.username= data.get('username')
        if data.get('password') is not None:
            user.password= data.get('password')

        db.session.commit()
        return jsonify({'status':200, "message":"changes done!!"})

    else:
        return jsonify({'status':404, 'message':'wrong request method!!'}),404


@app.route('/update-dp', methods=['PUT'])
@login_required
def updateDp():
    """
      PUT: update current logged-in user's profile picture
      return: error status/200 on successful update
    """
    if request.method == "PUT":
        user = User.query.filter_by(email= current_user.email).first()
        data = request.files
        print(data)
        if data.get('image') is not None:
            image = data.get('image')
            filepath = image.filename
            image.save(f"./static/uploads/images/{filepath}")
            user.image= filepath
            db.session.commit()
            return jsonify({'status':200, "message":"changes done!!"})
        else:
            return jsonify({'status':500, "message":"image not found in request!!"})

    else:
        return jsonify({'status':404, 'message':'wrong request method!!'}),404


@app.route('/user', methods=['GET'])
@login_required
def getUser():
    """
      GET: update current logged-in user's info
      return: error status/200 on successful fetch
    """
    user = User.query.get(current_user.email)
    if user is not None:
        return jsonify({'status':200, "userInfo":user.serialize})
    else:
          return jsonify({'status':404, 'message':'please login first!!'}),404


@app.route('/delete-user', methods=['DELETE'])
@login_required
def deleteUser():
    """
      DELETE: deletes current logged-in user from DB
      return: error status/200 on successful delete
    """
    if request.method == 'DELETE':
        user = User.query.get(current_user.email)
        if user is not None:
            User.query.filter_by(email=user.email).delete()
            db.session.commit()
            return jsonify({'status':200, 'message':'Your account has been deleted!!'})
        else:
            return jsonify({'status':404, 'message':'account does not exist!!'}),404
    else:
        return jsonify({'status':404, 'message':'Wrong request method!!'}),404


# ................user authentication..................... 3
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@app.route("/login", methods=["GET", "POST"])
def login():
    """
      GET: requests, display wrong request method code/message.
      POST: login the current user by processing the posted credentials.
      return: error code on error/ 200 on successful login
    """
    if request.method=='POST':
        data = request.get_json()
        user = User.query.get(data.get('email'))
        if user is not None:
            if user.password == data.get('password'):
                user.authenticated = True
                db.session.add(user)
                db.session.commit()
                login_user(user, remember=True)
                return jsonify({'status':200, 'message':"successful logged in!!"})
            else:
                return jsonify({'status':404, 'message':'Wrong credential(s)!!'}),404
        else:
            return jsonify({'status':404, 'message':'user does not exist!!'}),404
    else:
        return jsonify({'status':500, 'message':'Wrong Request Method!!'}),500


@app.route("/logout", methods=["GET"])
@login_required
def logout():
    """Logout the current user."""
    user = current_user
    user.authenticated = False
    db.session.add(user)
    db.session.commit()
    logout_user()
    return jsonify({'status':200, 'message':'successfuly logged out!!'})


# .......................Starting the application.................... #


if __name__ == '__main__':
  app.run(debug=True)
