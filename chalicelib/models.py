from __future__ import annotations

import os
import time
from datetime import datetime
from typing import List, Optional
from uuid import uuid4

import boto3
from mypy_boto3_s3 import S3Client
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.orm.session import Session
from sqlalchemy.sql.schema import ForeignKey, Sequence, Table

from chalicelib.datadefs import PresignedUploadResponse

Base = declarative_base()

image_tags = Table(
    "image_tags",
    Base.metadata,
    Column("image_id", ForeignKey("images.id"), primary_key=True),
    Column("tag_id", ForeignKey("tags.id"), primary_key=True),
)


class Image(Base):
    __tablename__ = "images"

    # \/ \/ ideally these would come from a config object \/ \/
    BUCKET_NAME = os.environ["BUCKET_NAME"]
    PRESIGNED_URL_EXPIRY = 3600  # in seconds, i.e. 1 hour

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

    def generate_prefix(self) -> str:
        dt = datetime.fromtimestamp(self.created_timestamp)
        date_part = dt.strftime("%Y/%m/%d/%H-%M")
        return f"{date_part}-{uuid4()}/"

    @classmethod
    def from_upload(
        cls,
        session: Session,
        created_by: str,
        filename: str,
        image_data: bytes,
        tags: List[Tag],
    ) -> Image:
        size = len(image_data)

        image = cls(
            filename=filename,
            created_by=created_by,
            size=size,
            tags=tags,
            created_timestamp=int(time.time()),
        )
        image.prefix = image.generate_prefix()
        s3_client: S3Client = boto3.client("s3")

        # # TODO: best practice to set the content-type when uploading the object, otherwise it's application/octet-stream
        # s3_client.put_object(
        #     Bucket=cls.BUCKET_NAME,
        #     Key=f"{image.prefix}/{image.filename}",
        #     Body=image_data,
        # )

        image.upload_timestamp = int(time.time())
        session.add(image)
        session.commit()
        return image

    @classmethod
    def prepare_upload_url(
        cls,
        session: Session,
        created_by: str,
        filename: str,
        size: int,
        tags: List[Tag],
    ) -> PresignedUploadResponse:
        image = cls(
            filename=filename,
            created_by=created_by,
            size=size,
            tags=tags,
            created_timestamp=int(time.time()),
        )
        image.prefix = image.generate_prefix()
        session.add(image)
        session.commit()
        s3_client: S3Client = boto3.client("s3")
        url = s3_client.generate_presigned_url(
            "put_object",
            Params={
                "Bucket": cls.BUCKET_NAME,
                "Key": f"{image.prefix}/{image.filename}",
            },
            ExpiresIn=cls.PRESIGNED_URL_EXPIRY,
        )
        return PresignedUploadResponse(image.id, url)

    def to_payload(self):
        url: Optional[str] = None
        if self.upload_timestamp is not None:
            s3_client: S3Client = boto3.client("s3")
            url = s3_client.generate_presigned_url(
                "get_object",
                Params={
                    "Bucket": self.BUCKET_NAME,
                    "Key": f"{self.prefix}{self.filename}",
                },
                ExpiresIn=self.PRESIGNED_URL_EXPIRY,
            )

        return {
            "id": self.id,
            "created_by": self.created_by,
            "created_timestamp": self.created_timestamp,
            "filename": self.filename,
            "size": self.size,
            "tags": [tag.to_payload() for tag in self.tags],
            "uploaded_timestamp": self.upload_timestamp,
            "url": url,
        }


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
