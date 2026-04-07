import uuid
from sqlalchemy.dialects.postgresql import UUID

from db import db


class MagicalSchool(db.Model):
    __tablename__ = "magical_schools"

    school_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    school_name = db.Column(db.String(255), unique=True, nullable=False)
    location = db.Column(db.String(255))
    founded_year = db.Column(db.Integer)
    headmaster = db.Column(db.String(255))

    wizards = db.relationship(
        "Wizard",
        back_populates="school",
    )
    books = db.relationship(
        "Book",
        back_populates="school",
    )

    def __init__(self, school_name, location=None, founded_year=None, headmaster=None):
        self.school_name = school_name
        self.location = location
        self.founded_year = founded_year
        self.headmaster = headmaster
