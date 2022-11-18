from pydantic import BaseModel, EmailStr, constr, validator

from bookmarker.config import get_settings


class RegistrationForm(BaseModel):
    username: str
    # password: constr(min_length=8)
    password: str
    email: EmailStr | None

    @validator("password")
    def validate_password(cls, password):
        settings = get_settings()
        password = settings.PWD_CONTEXT.hash(password)
        return password


class RegistrationSuccess(BaseModel):
    message: str
