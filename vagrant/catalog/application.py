#!/usr/bin/env python
'''
This application is my submission for Project 2 of the Udacity Fullstack Development
NanoDegree program.  It will run up a server and website that will provide the user
with a list of books within a variety of different categories
'''
# Imports
from flask import Flask, render_template, request, redirect, jsonify, url_for, flash
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, Book, User
from flask import session as login_session
import random
import string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

app = Flask(__name__)

# Create a database session and connect to it
engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)


# Function for creating a database
def connect():
    session = DBSession()
    return session


# Functions for checking if a user exists in the database, or to create one if it does not
def createUser(login_session):
    try:
        session = connect()
        newUser = User(name=login_session['username'], email=login_session['email'], picture=login_session['picture'])
        session.add(newUser)
        session.commit()
        user = session.query(User).filter_by(email=login_session['email']).one()
        return user.id
    finally:
        session.close()


def getUserInfo(user_id):
    try:
        session = connect()
        user = session.query(User).filter_by(id=user_id).one()
        return user
    finally:
        session.close()


def getUserId(email):
    try:
        session = connect()
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None


# JSON API Endpoints for viewing book information
@app.route('/category/JSON')
def allBooksJSON():
    try:
        session = connect()
        allBooks = session.query(Book).all()
        return jsonify(AllBooks=[i.serialize for i in allBooks])
    finally:
        session.close()


@app.route('/category/<int:category_id>/JSON')
def categoryBooksJSON(category_id):
    try:
        session = connect()
        books = session.query(Book).filter_by(category_id=category_id).all()
        return jsonify(Books=[i.serialize for i in books])
    finally:
        session.close()


@app.route('/book/<int:book_id>/JSON')
def bookJSON(book_id):
    try:
        session = connect()
        book = session.query(Book).filter_by(id=book_id).one()
        return jsonify(Book=[book.serialize])
    finally:
        session.close()


# Create a new category
@app.route('/category/new/', methods=['GET', 'POST'])
def newCategory():
    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        newCategory = Category(name=request.form['name'], user_id=login_session['user_id'])
        try:
            session = connect()
            session.add(newCategory)
            flash('New Category %s Successfully Created' % newCategory.name)
            session.commit()
            return redirect(url_for('showMainPage'))
        finally:
            session.close()
    else:
        return render_template('newCategory.html')


# Create a new Book
@app.route('/book/new/<int:category_id>/', methods=['GET', 'POST'])
def newBook(category_id):
    if 'username' not in login_session:
        return redirect('/login')
    try:
        session = connect()
        category = session.query(Category).filter_by(id=category_id).one()
        if request.method == 'POST':
            newBook = Book(name=request.form['name'], category_id=category.id, description=request.form['description'], user_id=category.user_id)
            try:
                session.add(newBook)
                session.commit()
                return redirect(url_for('showMainPage'))
            finally:
                session.close()
        else:
            return render_template('newBook.html', category_id=category_id)
    finally:
        session.close()


# Route for editing books
@app.route('/category/<int:category_id>/book/<int:book_id>/edit/', methods=['GET', 'POST'])
def editBook(book_id, category_id):
    if 'username' not in login_session:
        return redirect('/login')
    try:
        session = connect()
        bookToEdit = session.query(Book).filter_by(id=book_id).one()
        if login_session['user_id'] != bookToEdit.user_id:
            flash("You do not have authorization to edit this book!")
            return render_template('bookDescription.html', book=bookToEdit)
        if request.method == 'POST':
            if request.form['name']:
                bookToEdit.name = request.form['name']
            if request.form['description']:
                bookToEdit.description = request.form['description']
            session.add(bookToEdit)
            session.commit()
            return render_template('bookDescription.html', book=bookToEdit)
        else:
            return render_template('editBook.html', book=bookToEdit)
    finally:
        session.close()


# Route for deleting a book
@app.route('/category/<int:category_id>/book/<int:book_id>/delete', methods=['GET', 'POST'])
def deleteBook(category_id, book_id):
    if 'username' not in login_session:
        return redirect('/login')
    try:
        session = connect()
        bookToDelete = session.query(Book).filter_by(id=book_id).one()
        if login_session['user_id'] != bookToDelete.user_id:
            flash("You do not have authorization to delete this book!")
            return render_template('bookDescription.html', book=bookToDelete)
        if request.method == 'POST':
            session.delete(bookToDelete)
            session.commit()
            return redirect(url_for('showMainPage'))
        else:
            return render_template('deleteBook.html', book=bookToDelete)
    finally:
        session.close()


# Route for editing an existing category
@app.route('/category/<int:category_id>/edit', methods=['GET', 'POST'])
def editCategory(category_id):
    if 'username' not in login_session:
        return redirect('/login')
    try:
        session = connect()
        categoryToEdit = session.query(Category).filter_by(id=category_id).one()
        books = session.query(Book).filter_by(category_id=categoryToEdit.id).all()
        if login_session['user_id'] != categoryToEdit.user_id:
            flash("You do not have authorization to edit this category!")
            return render_template('displayCatBooks.html', category=categoryToEdit, books=books)
        if request.method == 'POST':
            if request.form['name']:
                categoryToEdit.name = request.form['name']
            session.add(categoryToEdit)
            session.commit()
            return redirect(url_for('showMainPage'))
        else:
            return render_template('editCategory.html', category=categoryToEdit)
    finally:
        session.close()


# Route for Logging in
@app.route('/login/')
def login():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)


@app.route('/')
def showMainPage():
    try:
        session = connect()
        categories = session.query(Category).all()
        books = session.query(Book).all()
        if 'username' not in login_session:
            return render_template("publicMainPage.html", categories=categories, books=books)
        else:
            return render_template("mainPage.html", categories=categories, books=books)
    finally:
        session.close()


@app.route('/category/books/<int:category_id>/')
def showCategoryBooks(category_id):
    try:
        session = connect()
        category = session.query(Category).filter_by(id=category_id).one()
        books = session.query(Book).filter_by(category_id=category.id).all()
        if 'username' not in login_session:
            return render_template("publicDisplayCatBooks.html", category=category, books=books)
        else:
            return render_template("displayCatBooks.html", category=category, books=books)
    finally:
        session.close()


@app.route('/books/<int:book_id>/')
def showBookDescription(book_id):
    try:
        session = connect()
        book = session.query(Book).filter_by(id=book_id).one()
        session.close()
        if 'username' not in login_session:
            return render_template("publicBookDescription.html", book=book)
        else:
            return render_template('bookDescription.html', book=book)
    finally:
        session.close()


@app.route('/fbconnect', methods=['POST'])
def fbconnect():
    # Verify the value of state, to guard against cross-site reference forgery attacks
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid State Paramater.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    access_token = request.data

    # Exchange the client token for long-lived server-side token
    app_id = json.loads(open('fb_client_secrets.json', 'r').read())['web']['app_id']
    app_secret = json.loads(open('fb_client_secrets.json', 'r').read())['web']['app_secret']
    url = 'https://graph.facebook.com/oauth/access_token?grant_type=fb_exchange_token&client_id=%s&client_secret=%s&fb_exchange_token=%s' % (app_id, app_secret, access_token)
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]

    # Use token to get user info from API
    # userinfo_url = "https://graph.facebook.com/v2.8/me" //Unsure of teh purpose of this code, which was included in the demo code
    '''
        Split the result from the server exchange first by commans, and select the first index
        which will give us the key:value for the server access token then we will split it on colons to pull
        out the actual token value and format it to be used directly in the graph API calls
    '''
    token = result.split(',')[0].split(':')[1].replace('"', '')

    url = 'https://graph.facebook.com/v2.8/me?access_token=%s&fields=name,id,email' % token

    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    data = json.loads(result)
    login_session['provider'] = 'facebook'
    login_session['username'] = data["name"]
    login_session['email'] = data["email"]
    login_session['facebook_id'] = data["id"]

    # Store the token in the login_session so that we can logout when requested
    login_session['access_token'] = token

    # Get user's picture
    url = 'https://graph.facebook.com/v2.8/me/picture?access_token=%s&redirect=0&height=200&width=200' % token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    data = json.loads(result)
    login_session['picture'] = data["data"]["url"]

    # See if user currently exists in database, and add them if they do not
    user_id = getUserId(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '

    flash("Now logged in as %s" % login_session['username'])
    render_template('login.html')
    return output


@app.route('/disconnect')
def disconnect():
    try:
        facebook_id = login_session['facebook_id']
        access_token = login_session['access_token']
        url = 'https://graph.facebook.com/%s/persmissions?access_token=%s' % (facebook_id, access_token)
        h = httplib2.Http()
        result = h.request(url, 'DELETE')[1]
        login_session.clear()
    finally:
        flash('You have been successfully logged out')
        return showMainPage()


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
