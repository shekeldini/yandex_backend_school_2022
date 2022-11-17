from re import compile

from pydantic import BaseModel, EmailStr, constr, validator

from bookmarker.config import get_settings


class RegistrationForm(BaseModel):
    # ERROR: очевидно, что пользователь не может использовать в качестве логина/пароля пустые строки.
    # Поэтому тут следовало добавить валидацию и соответствующие тесты на неё.
    username: constr(min_length=3, strip_whitespace=True)
    password: constr(min_length=8)
    email: EmailStr | None

    @classmethod
    def _check_by_regexp(cls, password: str) -> None:
        # Здесь можно использовать любые валидаторы, которые посчитаете нужными.
        # Это пример того, как можно сделать сообщения об ошибках, понятные пользователю.

        char_regex = compile(r"(\w{8,})")
        lower_regex = compile(r"[a-z]+")
        upper_regex = compile(r"[A-Z]+")
        digit_regex = compile(r"[0-9]+")
        space_symbols_regex = compile(r"[^\S\n\t]+")
        other_symbols_regex = compile(r"[\W+]+")

        if not char_regex.findall(password):
            raise ValueError("Password must contain at least 8 characters")
        elif not lower_regex.findall(password):
            raise ValueError("Password must contain at least one lowercase character")
        elif not upper_regex.findall(password):
            raise ValueError("Password must contain at least one uppercase character")
        elif not digit_regex.findall(password):
            raise ValueError("Password must contain at least one digit character")
        elif space_symbols_regex.findall(password):
            raise ValueError("Password mustn't contain spaces")
        elif other_symbols_regex.findall(password):
            raise ValueError("Password must contain only A-Z, a-z, 0-9 and _")

    @validator("password")
    def validate_password(cls, password):
        cls._check_by_regexp(password)
        settings = get_settings()
        password = settings.PWD_CONTEXT.hash(password)
        return password


class RegistrationSuccess(BaseModel):
    message: str
