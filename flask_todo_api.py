from flask import Flask, jsonify, make_response, request
from flask_mongoengine import MongoEngine
import os

db_name = os.environ.get("MONGO_DB_NAME")

db_password = os.environ.get("MONGO_DB_PASS")

DB_URI = f"mongodb+srv://aayush:{db_password}@flask-todo.b7xrj.mongodb.net/{db_name}?retryWrites=true&w=majority"

db = MongoEngine()

app = Flask(__name__)
app.config['MONGODB_HOST'] = DB_URI
db.init_app(app)


# Schema
class Book(db.Document):
    name = db.StringField()
    author = db.StringField()


# Methods
@app.route('/books/createBook', methods=['POST'])
# Function for creating book
def create_book():
    book_content = request.get_json()
    book = Book(name=book_content['name'],
                author=book_content['author']).save()
    return make_response(jsonify(message="Successfully Created!!", book=book), 201)


@app.route('/books', methods=['GET'])
# Function for fetching all book
def fetch_book():
    book = Book.objects()
    return make_response(jsonify(book=book), 200)


@app.route('/books/<book_id>', methods=['PUT'])
# Function for updating a book
def update_book(book_id):
    book_content = request.json
    book = Book.objects(id=book_id).first()
    book.update(name=book_content['name'],
                author=book_content['author'])
    return make_response(jsonify(message="Updated Successfully"), 200)


@app.route('/books/<book_id>', methods=['DELETE'])
# Function for deleting a book
def delete_book(book_id):
    book = Book.objects(id=book_id).first()
    book.delete()
    return make_response(jsonify(message="Deleted Successfully"), 200)


if __name__ == '__main__':
    app.run(debug=True)
