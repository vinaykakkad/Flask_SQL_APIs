# Import data from a csv file into our database.

import os, csv
from flask import Flask
from env import SQLALCHEMY_DATABASE_URI
from app.models import *

app=Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"]= SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False

db.init_app(app)

def main():
    counter=0
    f = open("books.csv")
    reader = csv.reader(f)
    for isbn, title, author, year in reader:
        book = Books(isbn=isbn, title=title, author=author, year=int(float(year)), views=0)
        db.session.add(book)
        counter+=1
    db.session.commit()
    print(counter)

if __name__=="__main__":
    with app.app_context():     #flask apps run on web,this line because we have to run flask in cmd
        main()
