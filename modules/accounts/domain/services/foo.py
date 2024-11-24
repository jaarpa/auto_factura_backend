from modules.accounts.domain.entities.user import User


def bar() -> User:
    return User(
        email="email@mail.com",
    )
