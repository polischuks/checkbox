from app.core.config import settings


def test_create_receipt(client, logged_user):
    """Test creating a receipt with a single item.

    The item is a product with id 2 and quantity 1.
    The payment type is card and the payment amount is 620000."""
    data = {
        "user_id": 2,
        "sale_items": [
            {
                "product_id": 2,
                "quantity": 1
            }
        ],
        "payment_type": "card",
        "payment_amount": 620000
    }
    response = client.post(f"http://{settings.DOMAIN}:8000/receipts/", headers=logged_user, json=data)
    assert response.status_code == 200
    receipt = response.json()
    assert receipt["payment_amount"] == 620000
    assert receipt["payment_type"] == "card"
    assert receipt["change_given"] == 0


def test_cant_create_receipt_for_other_user(client):
    """Test that a user can't create a receipt for another user.

    The user is not authenticated, so the request should fail with 401 Unauthorized."""
    data = {
        "user_id": 1,
        "sale_items": [
            {
                "product_id": 2,
                "quantity": 1
            }
        ],
        "payment_type": "card",
        "payment_amount": 620000
    }
    response = client.post(f"http://{settings.DOMAIN}:8000/receipts/", json=data)
    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"


def test_get_receipts(client, logged_user):
    """Test getting all receipts for a user.

    The user has id 2 and has receipts in the database."""
    response = client.get(f"http://{settings.DOMAIN}:8000/receipts/", headers=logged_user)
    assert response.status_code == 200
    receipts = response.json()
    assert len(receipts) != 0


def test_get_receipt_by_id(client, logged_user):
    """Test getting a receipt by id.

    The receipt has id 2 and belongs to user with id 2."""
    response = client.get(f"http://{settings.DOMAIN}:8000/receipts/2", headers=logged_user)
    assert response.status_code == 200
    receipt = response.json()
    assert receipt["id"] == 2
    assert receipt["payment_amount"] == 2689830
    assert receipt["payment_type"] == "card"
    assert receipt["total"] == 2689830
    assert len(receipt["sale_items"]) == 1


def test_cant_get_receipt_by_id_for_other_user(client):
    """Test that a user can't get a receipt for another user.

    The user is not authenticated, so the request should fail with 401 Unauthorized."""
    response = client.get(f"http://{settings.DOMAIN}:8000/receipts/2")
    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"


def test_get_receipt_text(client, logged_user):
    """Test getting a receipt text by id.

    The receipt has id 2 and belongs to user with id 2."""
    expected_start = "ФОП Джонсонюк Борис Іванович ;)"
    expected_end = "========================================"
    response = client.get(f"http://{settings.DOMAIN}:8000/receipts/2/text", headers=logged_user)
    assert response.status_code == 200
    assert expected_start in response.text
    assert expected_end in response.text


def test_can_get_receipt_text_for_other_user(client):
    """Test that a user can get a receipt text for another user's receipt.

    This is needed when we send the link to the receipt."""
    response = client.get(f"http://{settings.DOMAIN}:8000/receipts/2/text")
    assert response.status_code == 200


def test_get_receipts_by_user(client, logged_user):
    """Test getting all receipts for a user.

    The user has id 2 and has receipts in the database."""
    response = client.get(f"http://{settings.DOMAIN}:8000/receipts", headers=logged_user)
    assert response.status_code == 200
    receipts = response.json()
    assert len(receipts) != 0
    for receipt in receipts:
        assert receipt["user_id"] == 2


def test_get_public_receipt(client):
    """Test getting a public receipt by id.

    The receipt has id 6 and is public."""
    response = client.get(f"http://{settings.DOMAIN}:8000/receipts/public/6")
    assert response.status_code == 200
    receipt = response.json()
    assert receipt["id"] == 6
    assert receipt["payment_amount"] == 1600000
    assert receipt["payment_type"] == "cash"
    assert receipt["total"] == 1516610
    assert len(receipt["sale_items"]) == 2
