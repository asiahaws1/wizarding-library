import uuid
from sqlalchemy.dialects.postgresql import UUID

from db import db


class Spell(db.Model):
    __tablename__ = "spells"

    spell_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    spell_name = db.Column(db.String(), unique=True, nullable=False)
    incantation = db.Column(db.String())
    difficulty_level = db.Column(db.Float())
    spell_type = db.Column(db.String())
    description = db.Column(db.String())

    specializations = db.relationship("WizardSpecialization", back_populates="spell")
    wizards = db.relationship(
        "Wizard",
        secondary="wizard_specializations",
        viewonly=True,
        back_populates="spells",
    )

    def __init__(
        self,
        spell_name,
        incantation=None,
        difficulty_level=None,
        spell_type=None,
        description=None,
    ):
        self.spell_name = spell_name
        self.incantation = incantation
        self.difficulty_level = difficulty_level
        self.spell_type = spell_type
        self.description = description
