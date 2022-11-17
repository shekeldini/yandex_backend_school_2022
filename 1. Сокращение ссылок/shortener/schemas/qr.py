from pydantic import BaseModel, Field, UUID4


class QRRequest(BaseModel):
    secret_key: UUID4 = Field(
        title="Secret key for short string"
    )
