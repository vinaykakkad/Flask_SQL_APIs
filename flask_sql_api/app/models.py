# 1. Importing DB from init.py.
# 2. Importing UserMixin as it adds function like is_authenticated, is_active, is_anonymous, get_id, to our models.
# 3. Importing security related function from werkezug
# 4. Importing func to perform queries like avg, sum, etc.

from . import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.sql import func

class Users(db.Model, UserMixin):
    __tablename__="users"

    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(100),nullable=False)
    password=db.Column(db.String(200),nullable=False)   # Password may be small, but it gets hashed to a long string in database

    def set_password(self, password):
        self.password=generate_password_hash(password, method='sha256')

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return self.username

class Books(db.Model):
    __tablename__="books"

    id=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(300), nullable=False)
    author=db.Column(db.String(100), nullable=False)
    isbn=db.Column(db.String(20), nullable=False)
    year=db.Column(db.Integer, nullable=False)
    views=db.Column(db.Integer, nullable=True)

    def get_number(self):                               # Returns the number of ratings that the book has received
        return Reviews.query.filter((Reviews.isbn==self.isbn) & (Reviews.rating != 0 )).count()

    def get_avg(self):
        avg=db.session.query(db.func.avg(Reviews.rating)).filter(Reviews.isbn==self.isbn).scalar()# Returns the average of ratings that the book has received
        if avg is None:
            return 0
        else:
            return round(avg,2)

    def get_revs(self):                                 # Returns all the reviews that the book has received
        all=Reviews.query.filter(Reviews.isbn==self.isbn).all()
        return all

    def set_views(self):                                # Every time the book is searched and viewed, views increase
        self.views+=1

class Reviews(db.Model):
    __tablename__="reviews"

    id=db.Column(db.Integer,primary_key=True)
    isbn=db.Column(db.String(20), nullable=False)
    username=db.Column(db.String(100),nullable=False)
    rating=db.Column(db.Integer, nullable=True, default=None)
    review=db.Column(db.Text, nullable=True, default=None)
