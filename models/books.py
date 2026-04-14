import uuid
from sqlalchemy.dialects.postgresql import UUID

from db import db


class Book(db.Model):
    __tablename__ = "books"

    book_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    school_id = db.Column(
        UUID(as_uuid=True),
        db.ForeignKey("schools.school_id"),
    )
    title = db.Column(db.String(), unique=True, nullable=False)
    author = db.Column(db.String())
    subject = db.Column(db.String())
    rarity_level = db.Column(db.Integer)
    magical_properties = db.Column(db.String())
    available = db.Column(db.Boolean(), default=True)

    school = db.relationship("School", back_populates="books")

    def __init__(
        self,
        school_id,
        title,
        author=None,
        subject=None,
        rarity_level=None,
        magical_properties=None,
        available=True,
    ):
        self.school_id = school_id
        self.title = title
        self.author = author
        self.subject = subject
        self.rarity_level = rarity_level
        self.magical_properties = magical_properties
        self.available = available
