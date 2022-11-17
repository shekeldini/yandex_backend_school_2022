from pydantic import BaseModel


class ServiceResponse(BaseModel):
    status_code: int
    text: str


def get_service_response() -> ServiceResponse:
    valid_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9." \
                  "eyJpZCI6InRlc3QiLCJ0aW1lc3RhbXAiOjB9." \
                  "RX8VMur1EMCF1cp8rlDuNn8jMsVyiSU8Mv00UbTGYZU"
    return ServiceResponse(
        status_code=200,
        text=valid_token
    )
