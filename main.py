from flask import Flask, render_template, request, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FloatField
from wtforms.validators import DataRequired, NumberRange
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.app_context().push()
app.config['SECRET_KEY'] = 'ShibaTailWag'
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///new-books-collection.db"
Bootstrap(app)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# Creating new Table called Book
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    author = db.Column(db.String(250), nullable=False)
    rating = db.Column(db.Float, nullable=False)

    # Optional: this will allow each book object to be identified by its title when printed.
    def __repr__(self):
        return f'<Book {self.title}>'


class LibraryForm(FlaskForm):
    title = StringField('Book Name:', validators=[DataRequired()])
    author = StringField('Book Author:', validators=[DataRequired()])
    rating = FloatField('Rating:', validators=[DataRequired(), NumberRange(min=0, max=10)])
    submit = SubmitField('Add Book')


class EditForm(FlaskForm):
    rating = FloatField('Rating:', validators=[DataRequired(), NumberRange(min=0, max=10)])
    submit = SubmitField('Update')


db.create_all()


@app.route('/')
def home():
    all_books = db.session.query(Book).all()
    return render_template('index.html', books=all_books)


@app.route("/add", methods=["GET", "POST"])
def add():
    form = LibraryForm()
    if form.validate_on_submit():
        new_book = Book(
            title=form.title.data,
            author=form.author.data,
            rating=form.rating.data
        )
        db.session.add(new_book)
        db.session.commit()

        return redirect(url_for('home'))
    return render_template('add.html', form=form)


@app.route("/edit/<book_id>", methods=["GET", "POST"])
def edit(book_id):
    form = EditForm()
    book = Book.query.get(book_id)
    if form.validate_on_submit():
        book.rating = form.rating.data
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('edit.html', book=book, form=form)


@app.route("/delete/<book_id>", methods=["GET"])
def delete(book_id):
    book = Book.query.get(book_id)
    db.session.delete(book)
    db.session.commit()
    return redirect(url_for('home'))


if __name__ == "__main__":
    app.run(debug=True)
