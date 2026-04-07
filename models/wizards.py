import uuid
from sqlalchemy.dialects.postgresql import UUID

from db import db


class Wizard(db.Model):
    __tablename__ = "wizards"

    wizard_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    school_id = db.Column(
        UUID(as_uuid=True),
        db.ForeignKey("magical_schools.school_id"),
    )
    wizard_name = db.Column(db.String(255), unique=True, nullable=False)
    house = db.Column(db.String(255))
    year_enrolled = db.Column(db.Integer)
    magical_power_level = db.Column(db.Integer)
    active = db.Column(db.Boolean, default=True)

    school = db.relationship("MagicalSchool", back_populates="wizards")
    specializations = db.relationship(
        "WizardSpecialization",
        back_populates="wizard",
    )
    spells = db.relationship(
        "Spell",
        secondary="wizard_specializations",
        viewonly=True,
        back_populates="wizards",
    )

    def __init__(
        self,
        wizard_name,
        school_id=None,
        house=None,
        year_enrolled=None,
        magical_power_level=None,
        active=True,
    ):
        self.school_id = school_id
        self.wizard_name = wizard_name
        self.house = house
        self.year_enrolled = year_enrolled
        self.magical_power_level = magical_power_level
        self.active = active
