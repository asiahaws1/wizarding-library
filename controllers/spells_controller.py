import uuid

from flask import jsonify, request

from db import db
from models.spells import Spell
from models.wizard_specializations import WizardSpecialization


def create_spell():
    post_data = request.form if request.form else request.get_json() or {}
    fields = ["spell_name", "incantation", "difficulty_level", "spell_type", "description"]
    required_fields = ["spell_name"]
    values = {}
    for field in fields:
        field_data = post_data.get(field)
        if field in required_fields and not field_data:
            return jsonify({"message": f"{field} is required"}), 400
        values[field] = field_data
    spell = Spell(
        spell_name=values["spell_name"],
        incantation=values["incantation"],
        difficulty_level=values["difficulty_level"],
        spell_type=values["spell_type"],
        description=values["description"],
    )
    db.session.add(spell)
    try:
        db.session.commit()
    except Exception:
        db.session.rollback()
        return jsonify({"message": "unable to create record"}), 400
    spell_result = {
        "spell_id": str(spell.spell_id),
        "spell_name": spell.spell_name,
        "incantation": spell.incantation,
        "difficulty_level": spell.difficulty_level,
        "spell_type": spell.spell_type,
        "description": spell.description,
    }
    return jsonify({"message": "spell created", "result": spell_result}), 201


def get_spells():
    query = db.session.query(Spell).all()
    spells = []
    for spell in query:
        spells.append(
            {
                "spell_id": str(spell.spell_id),
                "spell_name": spell.spell_name,
                "incantation": spell.incantation,
                "difficulty_level": spell.difficulty_level,
                "spell_type": spell.spell_type,
                "description": spell.description,
            }
        )
    return jsonify({"message": "spells found", "results": spells}), 200


def get_spells_by_difficulty(difficulty_level):
    try:
        difficulty_value = float(difficulty_level)
    except ValueError:
        return jsonify({"message": "difficulty_level must be a number"}), 400
    query = db.session.query(Spell).filter(Spell.difficulty_level == difficulty_value).all()
    spells = []
    for spell in query:
        spells.append(
            {
                "spell_id": str(spell.spell_id),
                "spell_name": spell.spell_name,
                "incantation": spell.incantation,
                "difficulty_level": spell.difficulty_level,
                "spell_type": spell.spell_type,
                "description": spell.description,
            }
        )
    return jsonify({"message": "spells found", "results": spells}), 200


def update_spell(spell_id):
    post_data = request.form if request.form else request.get_json() or {}
    try:
        spell_uuid = uuid.UUID(spell_id)
    except ValueError:
        return jsonify({"message": f"spell by id {spell_id} does not exist"}), 404
    query = db.session.query(Spell).filter(Spell.spell_id == spell_uuid).first()
    if not query:
        return jsonify({"message": f"spell by id {spell_id} does not exist"}), 404
    query.spell_name = post_data.get("spell_name", query.spell_name)
    query.incantation = post_data.get("incantation", query.incantation)
    query.difficulty_level = post_data.get("difficulty_level", query.difficulty_level)
    query.spell_type = post_data.get("spell_type", query.spell_type)
    query.description = post_data.get("description", query.description)
    try:
        db.session.commit()
    except Exception:
        db.session.rollback()
        return jsonify({"message": "unable to update record"}), 400
    updated = db.session.query(Spell).filter(Spell.spell_id == spell_uuid).first()
    spell_result = {
        "spell_id": str(updated.spell_id),
        "spell_name": updated.spell_name,
        "incantation": updated.incantation,
        "difficulty_level": updated.difficulty_level,
        "spell_type": updated.spell_type,
        "description": updated.description,
    }
    return jsonify({"message": "spell updated", "result": spell_result}), 200


def delete_spell(spell_id):
    try:
        spell_uuid = uuid.UUID(spell_id)
    except ValueError:
        return jsonify({"message": f"spell by id {spell_id} does not exist"}), 404
    query = db.session.query(Spell).filter(Spell.spell_id == spell_uuid).first()
    if not query:
        return jsonify({"message": f"spell by id {spell_id} does not exist"}), 404
    specializations = db.session.query(WizardSpecialization).filter(
        WizardSpecialization.spell_id == spell_uuid
    ).all()
    for specialization in specializations:
        db.session.delete(specialization)
    try:
        db.session.delete(query)
        db.session.commit()
    except Exception:
        db.session.rollback()
        return jsonify({"message": "unable to delete record"}), 400
    return jsonify({"message": "spell and related records deleted"}), 200
