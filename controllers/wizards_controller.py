from datetime import datetime
import uuid

from flask import jsonify, request

from db import db
from models.wizards import Wizard
from models.wizard_specializations import WizardSpecialization
from models.spells import Spell


def create_wizard():
    post_data = request.form if request.form else request.get_json() or {}
    fields = ["school_id", "wizard_name", "house", "year_enrolled", "magical_power_level", "active"]
    required_fields = ["wizard_name"]
    values = {}
    for field in fields:
        field_data = post_data.get(field)
        if field in required_fields and not field_data:
            return jsonify({"message": f"{field} is required"}), 400
        values[field] = field_data
    school_uuid = None
    if values["school_id"]:
        try:
            school_uuid = uuid.UUID(values["school_id"])
        except ValueError:
            return jsonify({"message": "school_id is invalid"}), 400
    wizard = Wizard(
        school_id=school_uuid,
        wizard_name=values["wizard_name"],
        house=values["house"],
        year_enrolled=values["year_enrolled"],
        magical_power_level=values["magical_power_level"],
        active=values["active"] if values["active"] is not None else True,
    )
    db.session.add(wizard)
    try:
        db.session.commit()
    except Exception:
        db.session.rollback()
        return jsonify({"message": "unable to create record"}), 400
    wizard_result = {
        "wizard_id": str(wizard.wizard_id),
        "school_id": str(wizard.school_id) if wizard.school_id else None,
        "wizard_name": wizard.wizard_name,
        "house": wizard.house,
        "year_enrolled": wizard.year_enrolled,
        "magical_power_level": wizard.magical_power_level,
        "active": wizard.active,
    }
    return jsonify({"message": "wizard created", "result": wizard_result}), 201


def get_wizards():
    query = db.session.query(Wizard).all()
    wizards = []
    for wizard in query:
        wizards.append(
            {
                "wizard_id": str(wizard.wizard_id),
                "school_id": str(wizard.school_id) if wizard.school_id else None,
                "wizard_name": wizard.wizard_name,
                "house": wizard.house,
                "year_enrolled": wizard.year_enrolled,
                "magical_power_level": wizard.magical_power_level,
                "active": wizard.active,
            }
        )
    return jsonify({"message": "wizards found", "results": wizards}), 200


def get_active_wizards():
    query = db.session.query(Wizard).filter(Wizard.active == True).all()
    wizards = []
    for wizard in query:
        wizards.append(
            {
                "wizard_id": str(wizard.wizard_id),
                "school_id": str(wizard.school_id) if wizard.school_id else None,
                "wizard_name": wizard.wizard_name,
                "house": wizard.house,
                "year_enrolled": wizard.year_enrolled,
                "magical_power_level": wizard.magical_power_level,
                "active": wizard.active,
            }
        )
    return jsonify({"message": "active wizards found", "results": wizards}), 200


def get_wizards_dynamic(value):
    if len(value) == 36:
        try:
            wizard_uuid = uuid.UUID(value)
        except ValueError:
            return jsonify({"message": f"wizard by id {value} does not exist"}), 404
        query = db.session.query(Wizard).filter(Wizard.wizard_id == wizard_uuid).first()
        if not query:
            return jsonify({"message": f"wizard by id {value} does not exist"}), 404
        wizard_result = {
            "wizard_id": str(query.wizard_id),
            "school_id": str(query.school_id) if query.school_id else None,
            "wizard_name": query.wizard_name,
            "house": query.house,
            "year_enrolled": query.year_enrolled,
            "magical_power_level": query.magical_power_level,
            "active": query.active,
        }
        return jsonify({"message": "wizard found", "result": wizard_result}), 200
    if value.isdigit():
        level = int(value)
        query = db.session.query(Wizard).filter(Wizard.magical_power_level == level).all()
        wizards = []
        for wizard in query:
            wizards.append(
                {
                    "wizard_id": str(wizard.wizard_id),
                    "school_id": str(wizard.school_id) if wizard.school_id else None,
                    "wizard_name": wizard.wizard_name,
                    "house": wizard.house,
                    "year_enrolled": wizard.year_enrolled,
                    "magical_power_level": wizard.magical_power_level,
                    "active": wizard.active,
                }
            )
        return jsonify({"message": "wizards found", "results": wizards}), 200
    query = db.session.query(Wizard).filter(Wizard.house == value).all()
    wizards = []
    for wizard in query:
        wizards.append(
            {
                "wizard_id": str(wizard.wizard_id),
                "school_id": str(wizard.school_id) if wizard.school_id else None,
                "wizard_name": wizard.wizard_name,
                "house": wizard.house,
                "year_enrolled": wizard.year_enrolled,
                "magical_power_level": wizard.magical_power_level,
                "active": wizard.active,
            }
        )
    return jsonify({"message": "wizards found", "results": wizards}), 200


def update_wizard(wizard_id):
    post_data = request.form if request.form else request.get_json() or {}
    try:
        wizard_uuid = uuid.UUID(wizard_id)
    except ValueError:
        return jsonify({"message": f"wizard by id {wizard_id} does not exist"}), 404
    query = db.session.query(Wizard).filter(Wizard.wizard_id == wizard_uuid).first()
    if not query:
        return jsonify({"message": f"wizard by id {wizard_id} does not exist"}), 404
    next_school_id = post_data.get("school_id", query.school_id)
    if isinstance(next_school_id, str):
        try:
            next_school_id = uuid.UUID(next_school_id)
        except ValueError:
            return jsonify({"message": "school_id is invalid"}), 400
    query.school_id = next_school_id
    query.wizard_name = post_data.get("wizard_name", query.wizard_name)
    query.house = post_data.get("house", query.house)
    query.year_enrolled = post_data.get("year_enrolled", query.year_enrolled)
    query.magical_power_level = post_data.get("magical_power_level", query.magical_power_level)
    query.active = post_data.get("active", query.active)
    try:
        db.session.commit()
    except Exception:
        db.session.rollback()
        return jsonify({"message": "unable to update record"}), 400
    updated = db.session.query(Wizard).filter(Wizard.wizard_id == wizard_uuid).first()
    wizard_result = {
        "wizard_id": str(updated.wizard_id),
        "school_id": str(updated.school_id) if updated.school_id else None,
        "wizard_name": updated.wizard_name,
        "house": updated.house,
        "year_enrolled": updated.year_enrolled,
        "magical_power_level": updated.magical_power_level,
        "active": updated.active,
    }
    return jsonify({"message": "wizard updated", "result": wizard_result}), 200


def delete_wizard(wizard_id):
    try:
        wizard_uuid = uuid.UUID(wizard_id)
    except ValueError:
        return jsonify({"message": f"wizard by id {wizard_id} does not exist"}), 404
    query = db.session.query(Wizard).filter(Wizard.wizard_id == wizard_uuid).first()
    if not query:
        return jsonify({"message": f"wizard by id {wizard_id} does not exist"}), 404
    specializations = db.session.query(WizardSpecialization).filter(
        WizardSpecialization.wizard_id == wizard_uuid
    ).all()
    for specialization in specializations:
        db.session.delete(specialization)
    try:
        db.session.delete(query)
        db.session.commit()
    except Exception:
        db.session.rollback()
        return jsonify({"message": "unable to delete record"}), 400
    return jsonify({"message": "wizard and related records deleted"}), 200


def create_specialization():
    post_data = request.form if request.form else request.get_json() or {}
    fields = ["wizard_id", "spell_id", "proficiency_level", "date_learned"]
    required_fields = ["wizard_id", "spell_id"]
    values = {}
    for field in fields:
        field_data = post_data.get(field)
        if field in required_fields and not field_data:
            return jsonify({"message": f"{field} is required"}), 400
        values[field] = field_data
    wizard_id = values["wizard_id"]
    spell_id = values["spell_id"]
    try:
        wizard_uuid = uuid.UUID(wizard_id)
        spell_uuid = uuid.UUID(spell_id)
    except ValueError:
        return jsonify({"message": "wizard_id or spell_id is invalid"}), 400
    wizard = db.session.query(Wizard).filter(Wizard.wizard_id == wizard_uuid).first()
    spell = db.session.query(Spell).filter(Spell.spell_id == spell_uuid).first()
    if not wizard or not spell:
        return jsonify({"message": "wizard or spell not found"}), 404
    proficiency_level = values["proficiency_level"]
    if proficiency_level is not None:
        try:
            proficiency_level = float(proficiency_level)
        except ValueError:
            return jsonify({"message": "proficiency_level must be a number"}), 400
        if proficiency_level < 1 or proficiency_level > 5:
            return jsonify({"message": "proficiency_level must be between 1 and 5"}), 400
    date_value = None
    if values["date_learned"]:
        try:
            date_value = datetime.fromisoformat(values["date_learned"])
        except ValueError:
            return jsonify({"message": "invalid date format"}), 400
    specialization = db.session.query(WizardSpecialization).filter(
        WizardSpecialization.wizard_id == wizard_uuid,
        WizardSpecialization.spell_id == spell_uuid,
    ).first()
    if specialization:
        specialization.proficiency_level = (
            proficiency_level if proficiency_level is not None else specialization.proficiency_level
        )
        if date_value:
            specialization.date_learned = date_value
    else:
        specialization = WizardSpecialization(
            wizard_id=wizard_uuid,
            spell_id=spell_uuid,
            proficiency_level=proficiency_level,
            date_learned=date_value,
        )
        db.session.add(specialization)
    try:
        db.session.commit()
    except Exception:
        db.session.rollback()
        return jsonify({"message": "unable to create record"}), 400
    specialization_result = {
        "wizard_id": str(specialization.wizard_id),
        "spell_id": str(specialization.spell_id),
        "proficiency_level": specialization.proficiency_level,
        "date_learned": specialization.date_learned.isoformat() if specialization.date_learned else None,
    }
    return jsonify({"message": "specialization saved", "result": specialization_result}), 201
