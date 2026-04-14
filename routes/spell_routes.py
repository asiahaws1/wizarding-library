from flask import Blueprint
from controllers import spells_controller as controllers

spell = Blueprint("spell", __name__)


@spell.route("/spell", methods=["POST"])
def create_spell():
    return controllers.create_spell()


@spell.route("/spells", methods=["GET"])
def get_spells():
    return controllers.get_spells()


@spell.route("/spells/<difficulty_level>", methods=["GET"])
def get_spells_by_difficulty(difficulty_level):
    return controllers.get_spells_by_difficulty(difficulty_level)


@spell.route("/spell/<spell_id>", methods=["PUT"])
def update_spell(spell_id):
    return controllers.update_spell(spell_id)


@spell.route("/spell/delete/<spell_id>", methods=["DELETE"])
def delete_spell(spell_id):
    return controllers.delete_spell(spell_id)
