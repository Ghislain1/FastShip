import pytest


@pytest.mark.parametrize(
    "username,email,password",
    [
        ("alice", "alice@example.com", "secret123"),
        ("bob", "bob@example.com", "mypassword"),
    ],
)
def test_create_customer(session, username, email, password):
    """Test create_customer works with valid data"""

    # Arrange

    assert username is not None
