import app.crud as crud
from app.schemas import UserCreate


def test_create_user(db_test):
    """Test create_user function."""

    user_data = UserCreate(name="John Doe", username="johndoe", password="securepassword123")
    user = crud.create_user(db_test, user_data)
    assert user.username == "johndoe"
    assert user.name == "John Doe"


def test_get_user_by_username(db_test):
    """Test get_user_by_username function."""

    user_data = UserCreate(name="John Doe", username="johndoe", password="securepassword123")
    created_user = crud.create_user(db_test, user_data)
    fetched_user = crud.get_user_by_username(db_test, "johndoe")
    assert fetched_user == created_user


def test_get_receipt_by_user_and_id(db_test):
    """Test get_receipt_by_user_and_id function."""

    fetched_receipt = crud.get_receipt_by_user_and_id(db_test, 6, 2)

    assert fetched_receipt.id == 6
    assert fetched_receipt.user_id == 2


