from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from flask_sqlalchemy import SQLAlchemy

# Create Flask app
app = Flask(__name__)

# Configure database with SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///new-books-collection.db'
db = SQLAlchemy(app)


# Define models
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    author = db.Column(db.String(250), unique=False, nullable=False)
    rating = db.Column(db.Float, unique=False, nullable=False)

    def __repr__(self):
        return f'<Book {self.title}>'


# Create the tables
with app.app_context():
    db.create_all()


all_books = []


@app.route('/')
def home():
    books = db.session.query(Book).all()
    return render_template("index.html", book_list=books)


@app.route("/add", methods=["GET", "POST"])
def add():

    if request.method == "POST":
        book = Book(
                title=request.form["title"],
                author=request.form["author"],
                rating=request.form["rating"]
                )
        db.session.add(book)
        db.session.commit()

        return redirect(url_for("home"))

    return render_template("add.html")


@app.route("/edit/<int:id_number>", methods=["GET", "POST"])
def edit(id_number):

    print(id_number)

    if request.method == "POST":
        # Get the new rating
        new_rating = request.form["rating"]
        # Update database with new rating
        book_to_update = Book.query.get(id_number)
        book_to_update.rating = new_rating
        db.session.commit()
        return redirect(url_for("home"))

    book_to_edit = Book.query.filter_by(id=id_number).first()

    return render_template("edit.html", book=book_to_edit)


if __name__ == "__main__":
    app.run(debug=True)

