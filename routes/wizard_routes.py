from flask import Blueprint
from controllers import wizards_controller as controllers

wizard = Blueprint("wizard", __name__)


@wizard.route("/wizard", methods=["POST"])
def create_wizard():
    return controllers.create_wizard()


@wizard.route("/wizards", methods=["GET"])
def get_wizards():
    return controllers.get_wizards()


@wizard.route("/wizards/active", methods=["GET"])
def get_active_wizards():
    return controllers.get_active_wizards()


@wizard.route("/wizards/<value>", methods=["GET"])
def get_wizards_dynamic(value):
    return controllers.get_wizards_dynamic(value)


@wizard.route("/wizard/<wizard_id>", methods=["PUT"])
def update_wizard(wizard_id):
    return controllers.update_wizard(wizard_id)


@wizard.route("/wizard/delete/<wizard_id>", methods=["DELETE"])
def delete_wizard(wizard_id):
    return controllers.delete_wizard(wizard_id)


@wizard.route("/wizard/specialize", methods=["POST"])
def create_specialization():
    return controllers.create_specialization()
