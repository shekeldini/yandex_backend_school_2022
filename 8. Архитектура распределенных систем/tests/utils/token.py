from random import choices, randint
from string import ascii_lowercase, ascii_uppercase, digits


def generate_id(length: int = 30) -> str:
    alphabet = ascii_lowercase + ascii_uppercase + digits + "_"
    return "".join(choices(alphabet, k=length))


def generate_timestamp() -> int:
    return randint(0, 2000000000)
