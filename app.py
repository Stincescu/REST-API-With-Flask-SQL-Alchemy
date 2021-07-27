from flask import Flask, request, jsonify 
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

#Flask to create instance of web app
#request to get request data
#jsonify to turn JSON output into a Response object with the application/json mimetype
#SQLAlchemy from flask-_sqlalchemy to accesing database
#Marshamallow from flask_marshallow to serialize and deserialize objects

# Init app
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__)) #to locate the sql file

# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir,'db.sqlite') #locate the db.sqlite in the current folder 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  #to avoid a warning in console

# Init db
db = SQLAlchemy(app)

# Init marshmallow
ma = Marshmallow(app)

# Book Class/Model
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True) #auto increment by 1
    title = db.Column(db.String(100),unique=True)
    author = db.Column(db.String(100))
    genre = db.Column(db.String(100))
    total_pages = db.Column(db.Integer)

    def __init__(self,title, author, genre, total_pages):
        self.title = title
        self.author = author
        self.genre = genre
        self.total_pages = total_pages


#Book Schema
class BookSchema(ma.Schema):
    class Meta:
        fields = ('id','title','author','genre','total_pages') #fields that are allowed to show

# Init schema
book_schema = BookSchema()
books_schema = BookSchema(many=True)

#Create the endpoints

# Create a book
@app.route('/book', methods = ['POST'])
def add_book():
    title = request.json['title']
    author = request.json['author']
    genre = request.json['genre']
    total_pages = request.json['total_pages']

    new_book = Book(title, author, genre, total_pages) #instantiating an object with what is coming from the client/Postman

    db.session.add(new_book) #add to the database
    db.session.commit()

    return book_schema.jsonify(new_book) #return to the client

#Get all books
@app.route('/book', methods = ['GET'])
def get_books():
    all_books = Book.query.all()
    result = books_schema.dump(all_books)
    return jsonify(result)

#Get a single book
@app.route('/book/<id>', methods = ['GET'])
def get_book(id):
    book = Book.query.get(id)
    return book_schema.jsonify(book)

#Update a book
@app.route('/book/<id>', methods = ['PUT'])
def update_book(id):
    book = Book.query.get(id)

    title = request.json['title']
    author = request.json['author']
    genre = request.json['genre']
    total_pages = request.json['total_pages']

    book.title = title
    book.author = author
    book.genre = genre
    book.total_pages = total_pages

    db.session.commit()

    return book_schema.jsonify(book)

#Delete Book
@app.route('/book/<id>', methods = ['DELETE'])
def delete_book(id):
    book = Book.query.get(id)
    db.session.delete(book)
    db.session.commit()
    return book_schema.jsonify(book)

#Run Server
if __name__ == '__main__':
    app.run(debug=True)

