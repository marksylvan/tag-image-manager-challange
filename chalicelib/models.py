from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.sql.schema import ForeignKey, Sequence, Table

Base = declarative_base()

image_tags = Table(
    "image_tags",
    Base.metadata,
    Column("image_id", ForeignKey("images.id"), primary_key=True),
    Column("tag_id", ForeignKey("tags.id"), primary_key=True),
)


class Image(Base):
    __tablename__ = "images"

    id = Column(Integer, Sequence("image_id_seq"), primary_key=True)

    filename = Column(String(160))
    created_by = Column(String(150))
    size = Column(Integer)
    created_timestamp = Column(Integer)
    upload_timestamp = Column(Integer, nullable=True)
    # yyyy/mm/dd/hh-mm-40ef85e8-87ee-46a2-982b-4fb8c37adcea/  = 54 chars
    # + 160 char filename
    prefix = Column(String(255), nullable=True)

    tags = relationship("Tag", secondary=image_tags, back_populates="images")


class Tag(Base):
    __tablename__ = "tags"

    id = Column(Integer, Sequence("tag_id_seq"), primary_key=True)
    name = Column(String(160))

    images = relationship(
        "Image", secondary=image_tags, back_populates="tags", lazy="dynamic"
    )

    def __repr__(self) -> str:
        return f"Tag (id={self.id}, name={self.name})"

    def to_payload(self):
        return {"id": self.id, "name": self.name}
