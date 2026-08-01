def test_show_top_page(client):
    response = client.get("/")

    assert response.status_code == 200

def test_show_register_page(client):
    response = client.get("/register")

    assert response.status_code == 200

def test_create_user(client):
    response = client.post(
        "/users/",
        json={
            "username": "testuser",
            "password": "password123",
        },
    )

    response_data = response.json()

    assert response.status_code == 201
    assert response_data["username"] == "testuser"
    assert "id" in response_data
    assert "password" not in response_data

def test_user_common_user_data(test_user):
    assert test_user["username"] == "testuser"

def test_user_common_room_data(test_room):
    assert test_room["room_name"] == "testroom"
    assert test_room["capacity"] == 10

def test_user_common_booking_data(test_booking, test_room):
    assert test_booking["room_id"] == test_room["id"]
    assert test_booking["reserved_num"] == 3