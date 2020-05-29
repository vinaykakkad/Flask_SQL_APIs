from flask import flash, request, render_template, make_response, redirect, url_for, jsonify
from flask_login import login_required, logout_user, current_user, login_user
from flask import current_app as app
from .models import db, Users, Books, Reviews
from . import login_manager
from sqlalchemy import desc
from env import GOODREADS_KEY
import requests

# A user_loader which is REQUIRED for login_manager
# This checks if the user is authenticated every time a page is loaded
@login_manager.user_loader
def load_user(user_id):
    if user_id is not None:
        return Users.query.get(user_id)
    return None


# This redirects to login page if someone tries to access the page that requires logging in
@login_manager.unauthorized_handler
def unauthorized():
    flash('You must be logged in to view that page.')
    return redirect(url_for('login'))

# To handle multiple requests
@app.teardown_appcontext
def shutdown_session(exception=None):
    db.session.remove()


# -------------The default route-------------------------
@app.route('/')
def default():
    return redirect(url_for('login'))


# -------------The LOGIN route-------------------------
@app.route('/login', methods=['GET','POST'])
def login():

        # If method is get and user is already logged in, redirects to dashboard, else to login page
    if request.method=='GET':
        if current_user.is_authenticated:
            return redirect(url_for('dashboard'))
        return render_template("login.htm")

        # If method is post, validates the login credentials
    if request.method=='POST':
        username=request.form.get('username')
        password=request.form.get('password')

        user=Users.query.filter(Users.username==username).first()
        if user is None:                                   # If username doesn't exist, return to login with that message
            msg="Invalid Username"
            return render_template("login.htm",msg=msg)
        else:
            if user.check_password(password):              # If username exists and password is correct, LOGIN USER and redirects to dashboard
                login_user(user)
                flash('Logged in successfully')
                return redirect(url_for('dashboard'))
            else:
                msg="Invlaid Password"                     # If username exists but password is incorrect, return to login page
                return render_template("login.htm",msg=msg)


# -------------The SIGNUP route-------------------------
@app.route('/signup', methods=['GET','POST'])
def signup():

        # If method is get and user is already logged in, redirects to dashboard, else to login page
    if request.method=='GET':
        if current_user.is_authenticated:
            return redirect(url_for('dashbaord'))
        return render_template("signup.htm")

    if request.method=='POST':
        username=request.form.get('username')
        password=request.form.get('password')
        c_password=request.form.get('c_password')

        existing_user = Users.query.filter(Users.username == username).first()
        if existing_user is None:
            if password==c_password:                        #If the user doesn't exist and password is confirmed, redirects to login page
                new_user=Users(username=username)
                new_user.set_password(password) #Here the password is hased and stored into the database
                db.session.add(new_user)
                db.session.commit()
                flash('Account created successfully!! Log in to continue')
                return redirect(url_for('login'))
            else:
                msg="The passwords did not match"           #If the user doesn't exist but password is not confirmed, return signup page with message
                return render_template("signup.htm", msg=msg)
        else:
            msg="User Already Exists"                       #If the user already exists, return signup page with message
            return render_template("signup.htm",msg=msg)


# -------------The DASHBOARD route( login req)-------------------------
@app.route('/dashboard', methods=['GET','POST'])
@login_required
def dashboard():

        # If method is get diplays most viewed books.
    if request.method=='GET':
        books=Books.query.order_by(Books.views.desc()).limit(10).all()
        msg="Most viewed books:"
        return render_template("dashboard.htm",current_user=current_user,books=books,msg=msg)
        # If request method is post, diplays required results
    if request.method=='POST':
        option=request.form.get('option')
        value=request.form.get('value')
        if option=="author":
            books=Books.query.filter(Books.author.like('%'+value+'%')).all()
        if option=="title":
            books=Books.query.filter(Books.title.like('%'+value+'%')).all()
        if option=="isbn":
            books=Books.query.filter(Books.isbn.like('%'+value+'%')).all()

        count=len(books)
        if count == 0:
            msg="No matched results!!"
        else:
            msg="Showing "+str(count)+" results:"
        return render_template("dashboard.htm",current_user=current_user,books=books,msg=msg)


# -------------The books route( login req)-------------------------
@app.route('/books/<string:code>', methods=['GET'])
@login_required
def books(code):
    book=Books.query.filter(Books.isbn==code).first()
    book.set_views()
    db.session.commit()
    res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key":GOODREADS_KEY, "isbns":code}) # Getting data from Goodreads API
    if res.status_code == 200:
        a=res.json()
        count=a['books'][0]['work_ratings_count']
        average=a['books'][0]['average_rating']
    else:
        count=None
        average=None
    return render_template("book.htm",book=book,count=count,average=average)


# -------------The logout_user route( login req)-------------------------
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


# -------------The post(reviews) route( login req)-------------------------
@app.route("/post/<string:isbn>/<string:user>",methods=['POST'])
@login_required
def post(isbn,user):
    rating=request.form.get('rating')
    review=request.form.get('review')

    rev=Reviews.query.filter((Reviews.isbn==isbn) & (Reviews.username==user)).all()
    if len(rev) == 0:
        review=Reviews(isbn=isbn, username=user, rating=int(rating), review=review)
        db.session.add(review)
        db.session.commit()
        flash('Review added successfully')
        return redirect(url_for('dashboard'))
    else:
        flash('You have already submiited your review')
        return redirect(url_for('dashboard'))

# -------------The API route-------------------------
@app.route("/api/<string:isbn>")
def api(isbn):
    book=Books.query.filter(Books.isbn==isbn).first()
    if book==None:
        return jsonify({"error": "Invalid isbn code"}), 422
    else:
        return jsonify({
              "isbn": book.isbn,
              "author": book.author,
              "title": book.title,
              "year": book.year,
              "rating_count": book.get_number(),
              "average_rating":float(book.get_avg())
          })
