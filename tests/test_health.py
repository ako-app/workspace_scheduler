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