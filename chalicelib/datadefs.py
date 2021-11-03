from dataclasses import dataclass


@dataclass
class PresignedUploadResponse:
    id: int
    upload_url: str

    def to_response(self):
        return {
            "id": self.id,
            "upload_url": self.upload_url,
        }
