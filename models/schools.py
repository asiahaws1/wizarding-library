import uuid
from sqlalchemy.dialects.postgresql import UUID

from db import db


class School(db.Model):
    __tablename__ = "schools"

    school_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    school_name = db.Column(db.String(), unique=True, nullable=False)
    location = db.Column(db.String())
    founded_year = db.Column(db.Integer)
    headmaster = db.Column(db.String())

    wizards = db.relationship("Wizard", back_populates="school")
    books = db.relationship("Book", back_populates="school")

    def __init__(self, school_name, location=None, founded_year=None, headmaster=None):
        self.school_name = school_name
        self.location = location
        self.founded_year = founded_year
        self.headmaster = headmaster
