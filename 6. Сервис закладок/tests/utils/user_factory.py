from secrets import choice
from string import ascii_lowercase, ascii_uppercase, digits

from factory import Factory, Faker


def generate_strong_password(length: int = 30):
    alphabet = ascii_lowercase + ascii_uppercase + digits + "_"
    return "".join(choice(alphabet) for _ in range(length))


class User:
    def __init__(self, **kwargs):
        self.username = kwargs.get("username")
        self.password = kwargs.get("password")
        self.email = kwargs.get("email")

    def __repr__(self):
        return "User(username='{s.username}', password='{s.password}', email='{s.email}')".format(s=self)


class UserFactory(Factory):
    class Meta:
        model = User

    username = Faker("first_name")
    password = generate_strong_password()
    email = Faker("email")
