from flask import Blueprint
from controllers import schools_controller as controllers

school = Blueprint("school", __name__)


@school.route("/school", methods=["POST"])
def create_school():
    return controllers.create_school()


@school.route("/schools", methods=["GET"])
def get_schools():
    return controllers.get_schools()


@school.route("/school/<school_id>", methods=["GET"])
def get_school(school_id):
    return controllers.get_school(school_id)


@school.route("/school/<school_id>", methods=["PUT"])
def update_school(school_id):
    return controllers.update_school(school_id)


@school.route("/school/delete/<school_id>", methods=["DELETE"])
def delete_school(school_id):
    return controllers.delete_school(school_id)
