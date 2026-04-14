import uuid

from flask import jsonify, request

from db import db
from models.schools import School
from models.wizards import Wizard
from models.books import Book


def create_school():
    post_data = request.form if request.form else request.get_json() or {}
    fields = ["school_name", "location", "founded_year", "headmaster"]
    required_fields = ["school_name"]
    values = {}
    for field in fields:
        field_data = post_data.get(field)
        if field in required_fields and not field_data:
            return jsonify({"message": f"{field} is required"}), 400
        values[field] = field_data
    school = School(
        school_name=values["school_name"],
        location=values["location"],
        founded_year=values["founded_year"],
        headmaster=values["headmaster"],
    )
    db.session.add(school)
    try:
        db.session.commit()
    except Exception:
        db.session.rollback()
        return jsonify({"message": "unable to create record"}), 400
    school_result = {
        "school_id": str(school.school_id),
        "school_name": school.school_name,
        "location": school.location,
        "founded_year": school.founded_year,
        "headmaster": school.headmaster,
    }
    return jsonify({"message": "school created", "result": school_result}), 201


def get_schools():
    query = db.session.query(School).all()
    schools = []
    for school in query:
        schools.append(
            {
                "school_id": str(school.school_id),
                "school_name": school.school_name,
                "location": school.location,
                "founded_year": school.founded_year,
                "headmaster": school.headmaster,
            }
        )
    return jsonify({"message": "schools found", "results": schools}), 200


def get_school(school_id):
    try:
        school_uuid = uuid.UUID(school_id)
    except ValueError:
        return jsonify({"message": f"school by id {school_id} does not exist"}), 404
    query = db.session.query(School).filter(School.school_id == school_uuid).first()
    if not query:
        return jsonify({"message": f"school by id {school_id} does not exist"}), 404
    school_result = {
        "school_id": str(query.school_id),
        "school_name": query.school_name,
        "location": query.location,
        "founded_year": query.founded_year,
        "headmaster": query.headmaster,
    }
    return jsonify({"message": "school found", "result": school_result}), 200


def update_school(school_id):
    post_data = request.form if request.form else request.get_json() or {}
    try:
        school_uuid = uuid.UUID(school_id)
    except ValueError:
        return jsonify({"message": f"school by id {school_id} does not exist"}), 404
    query = db.session.query(School).filter(School.school_id == school_uuid).first()
    if not query:
        return jsonify({"message": f"school by id {school_id} does not exist"}), 404
    query.school_name = post_data.get("school_name", query.school_name)
    query.location = post_data.get("location", query.location)
    query.founded_year = post_data.get("founded_year", query.founded_year)
    query.headmaster = post_data.get("headmaster", query.headmaster)
    try:
        db.session.commit()
    except Exception:
        db.session.rollback()
        return jsonify({"message": "unable to update record"}), 400
    updated = db.session.query(School).filter(School.school_id == school_uuid).first()
    school_result = {
        "school_id": str(updated.school_id),
        "school_name": updated.school_name,
        "location": updated.location,
        "founded_year": updated.founded_year,
        "headmaster": updated.headmaster,
    }
    return jsonify({"message": "school updated", "result": school_result}), 200


def delete_school(school_id):
    try:
        school_uuid = uuid.UUID(school_id)
    except ValueError:
        return jsonify({"message": f"school by id {school_id} does not exist"}), 404
    query = db.session.query(School).filter(School.school_id == school_uuid).first()
    if not query:
        return jsonify({"message": f"school by id {school_id} does not exist"}), 404
    books = db.session.query(Book).filter(Book.school_id == school_uuid).all()
    for book in books:
        db.session.delete(book)
    wizards = db.session.query(Wizard).filter(Wizard.school_id == school_uuid).all()
    for wizard in wizards:
        for specialization in wizard.specializations:
            db.session.delete(specialization)
        db.session.delete(wizard)
    try:
        db.session.delete(query)
        db.session.commit()
    except Exception:
        db.session.rollback()
        return jsonify({"message": "unable to delete record"}), 400
    return jsonify({"message": "school and related records deleted"}), 200
