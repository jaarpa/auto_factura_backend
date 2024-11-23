from modules.accounts.domain.services.foo import bar


def test_bar():
    user = bar()
    assert "email@mail.com" == user.email
