from pydantic import root_validator, BaseModel
from fastapi import status

from app.exceptions import NoId, NoTimeStamp


class CreateToken(BaseModel):
    id: str
    timestamp: int

    @root_validator
    def validate_values(cls, values):
        if values.get("id") is not None and values.get("timestamp") is not None:
            return values
        if values.get("id") is None:
            raise NoId(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Request is missing required query parameter 'id'"
            )

        if values.get("timestamp") is None:
            raise NoTimeStamp(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Request is missing required query parameter 'timestamp'"
            )

    def to_dict(self):
        return {
            "id": self.id,
            "timestamp": self.timestamp
        }
