from flask import Blueprint
from controllers import books_controller as controllers

book = Blueprint("book", __name__)


@book.route("/book", methods=["POST"])
def create_book():
    return controllers.create_book()


@book.route("/books", methods=["GET"])
def get_books():
    return controllers.get_books()


@book.route("/books/available", methods=["GET"])
def get_available_books():
    return controllers.get_available_books()


@book.route("/book/<book_id>", methods=["PUT"])
def update_book(book_id):
    return controllers.update_book(book_id)


@book.route("/book/delete/<book_id>", methods=["DELETE"])
def delete_book(book_id):
    return controllers.delete_book(book_id)
