import pytest
from backend.models.customer import Customer
from backend.services.customer_service import CustomerService
from backend.schemas.custom_schema import CustomerCreate


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
    service = CustomerService()
    customer_data = CustomerCreate(username=username, email=email, password=password)

    # Act
    result = service.create_customer(customer_data, session=session)

    # Assert
    assert result.username == username
    assert result.email == email
    assert result.hashed_password != password  # Should be hashed!
    assert result.id is not None
    assert result.is_active is True

    # Verify in database
    db_customer = session.get(Customer, result.id)
    assert db_customer is not None


def test_create_customer_duplicate_email(session):
    """Test duplicate email raises error"""
    service = CustomerService()

    # Create first customer
    _ = service.create_customer(
        CustomerCreate(username="alice", email="test@example.com", password="secret"),
        session=session,
    )

    # Try duplicate
    with pytest.raises(Exception):  # Unique constraint violation
        service.create_customer(
            CustomerCreate(username="bob", email="test@example.com", password="secret"),
            session=session,
        )


def test_load_customers_empty(session):
    """Test load_customers returns empty list when no customers"""
    service = CustomerService()
    customers = service.load_customers(session=session, offset=0, limit=1)
    assert len(customers) == 0


def test_load_customers_with_data(session):
    """Test load_customers returns all customers"""
    service = CustomerService()

    # Create 3 customers
    customers_data = [
        CustomerCreate(username="alice", email="alice@example.com", password="secret1"),
        CustomerCreate(username="bob", email="bob@example.com", password="secret2"),
        CustomerCreate(username="carol", email="carol@example.com", password="secret3"),
    ]

    for data in customers_data:
        service.create_customer(data, session=session)

    # Load all
    all_customers = service.load_customers(session, 0, 23)
    assert len(all_customers) == 3
    assert all_customers[0].username == "alice"
    assert all_customers[1].username == "bob"


def test_count_password_charater():
    """GHislain: Just count password charater"""
    cs = CustomerCreate(username="bob", email="test@example.com", password="secret")
    assert len(cs.password) == 6
