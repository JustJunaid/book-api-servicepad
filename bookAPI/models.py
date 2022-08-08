import datetime
from bookAPI import db


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
