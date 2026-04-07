import uuid

from flask import Blueprint, jsonify, request

from db import db
from models.books import Book

books_bp = Blueprint("books", __name__)


@books_bp.route("/book", methods=["POST"])
def create_book():
    post_data = request.form if request.form else request.get_json() or {}
    fields = ["school_id", "title", "author", "subject", "rarity_level", "magical_properties", "available"]
    required_fields = ["school_id", "title"]
    values = {}
    for field in fields:
        field_data = post_data.get(field)
        if field in required_fields and not field_data:
            return jsonify({"message": f"{field} is required"}), 400
        values[field] = field_data
    try:
        school_uuid = uuid.UUID(values["school_id"])
    except ValueError:
        return jsonify({"message": "school_id is invalid"}), 400
    book = Book(
        school_id=school_uuid,
        title=values["title"],
        author=values["author"],
        subject=values["subject"],
        rarity_level=values["rarity_level"],
        magical_properties=values["magical_properties"],
        available=values["available"] if values["available"] is not None else True,
    )
    db.session.add(book)
    try:
        db.session.commit()
    except Exception:
        db.session.rollback()
        return jsonify({"message": "unable to create record"}), 400
    book_result = {
        "book_id": str(book.book_id),
        "school_id": str(book.school_id) if book.school_id else None,
        "title": book.title,
        "author": book.author,
        "subject": book.subject,
        "rarity_level": book.rarity_level,
        "magical_properties": book.magical_properties,
        "available": book.available,
    }
    return jsonify({"message": "book created", "result": book_result}), 201


@books_bp.route("/books", methods=["GET"])
def get_books():
    query = db.session.query(Book).all()
    books = []
    for book in query:
        books.append(
            {
                "book_id": str(book.book_id),
                "school_id": str(book.school_id) if book.school_id else None,
                "title": book.title,
                "author": book.author,
                "subject": book.subject,
                "rarity_level": book.rarity_level,
                "magical_properties": book.magical_properties,
                "available": book.available,
            }
        )
    return jsonify({"message": "books found", "results": books}), 200


@books_bp.route("/books/available", methods=["GET"])
def get_available_books():
    query = db.session.query(Book).filter(Book.available == True).all()
    books = []
    for book in query:
        books.append(
            {
                "book_id": str(book.book_id),
                "school_id": str(book.school_id) if book.school_id else None,
                "title": book.title,
                "author": book.author,
                "subject": book.subject,
                "rarity_level": book.rarity_level,
                "magical_properties": book.magical_properties,
                "available": book.available,
            }
        )
    return jsonify({"message": "available books found", "results": books}), 200


@books_bp.route("/book/<book_id>", methods=["PUT"])
def update_book(book_id):
    post_data = request.form if request.form else request.get_json() or {}
    try:
        book_uuid = uuid.UUID(book_id)
    except ValueError:
        return jsonify({"message": f"book by id {book_id} does not exist"}), 404
    query = db.session.query(Book).filter(Book.book_id == book_uuid).first()
    if not query:
        return jsonify({"message": f"book by id {book_id} does not exist"}), 404
    next_school_id = post_data.get("school_id", query.school_id)
    if isinstance(next_school_id, str):
        try:
            next_school_id = uuid.UUID(next_school_id)
        except ValueError:
            return jsonify({"message": "school_id is invalid"}), 400
    query.school_id = next_school_id
    query.title = post_data.get("title", query.title)
    query.author = post_data.get("author", query.author)
    query.subject = post_data.get("subject", query.subject)
    query.rarity_level = post_data.get("rarity_level", query.rarity_level)
    query.magical_properties = post_data.get("magical_properties", query.magical_properties)
    query.available = post_data.get("available", query.available)
    try:
        db.session.commit()
    except Exception:
        db.session.rollback()
        return jsonify({"message": "unable to update record"}), 400
    updated = db.session.query(Book).filter(Book.book_id == book_uuid).first()
    book_result = {
        "book_id": str(updated.book_id),
        "school_id": str(updated.school_id) if updated.school_id else None,
        "title": updated.title,
        "author": updated.author,
        "subject": updated.subject,
        "rarity_level": updated.rarity_level,
        "magical_properties": updated.magical_properties,
        "available": updated.available,
    }
    return jsonify({"message": "book updated", "result": book_result}), 200


@books_bp.route("/book/delete/<book_id>", methods=["DELETE"])
def delete_book(book_id):
    try:
        book_uuid = uuid.UUID(book_id)
    except ValueError:
        return jsonify({"message": f"book by id {book_id} does not exist"}), 404
    query = db.session.query(Book).filter(Book.book_id == book_uuid).first()
    if not query:
        return jsonify({"message": f"book by id {book_id} does not exist"}), 404
    try:
        db.session.delete(query)
        db.session.commit()
    except Exception:
        db.session.rollback()
        return jsonify({"message": "unable to delete record"}), 400
    return jsonify({"message": "book and related records deleted"}), 200
