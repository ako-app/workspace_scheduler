def test_show_top_page(client):
    response = client.get("/")

    assert response.status_code == 200


def test_show_register_page(client):
    response = client.get("/register")

    assert response.status_code == 200


def test_user_common_user_data(test_user):
    assert test_user["username"] == "testuser"


def test_user_common_room_data(test_room):
    assert test_room["room_name"] == "testroom"
    assert test_room["capacity"] == 10


def test_user_common_booking_data(test_booking, test_room):
    assert test_booking["room_id"] == test_room["id"]
    assert test_booking["reserved_num"] == 3


# ユーザー
def test_create_user(client):
    """ユーザー登録に成功するテスト"""
    response = client.post(
        "/users/",
        json={
            "username": "testuser",
            "password": "password123",
        },
    )

    assert response.status_code == 201

    response_data = response.json()
    assert response_data["username"] == "testuser"
    assert "id" in response_data
    assert "password" not in response_data


def test_create_duplicate_user(client, test_user):
    """同じユーザー名の登録に失敗するテスト"""
    response = client.post(
        "/users/",
        json={
            "username": "testuser",
            "password": "password123",
        },
    )

    assert response.status_code == 409

    response_data = response.json()

    assert response_data["detail"] == "このユーザー名はすでに使用されています"


def test_login(client, test_user):
    """ログインに成功するテスト"""
    response = client.post(
        "/auth/login",
        data={
            "username": "testuser",
            "password": "password123",
        },
    )
    assert response.status_code == 200

    response_data = response.json()

    assert "access_token" in response_data
    assert response_data["token_type"] == "bearer"


def test_login_with_wrong_password(client, test_user):
    """誤ったパスワードでログインに失敗するテスト"""
    response = client.post(
        "/auth/login",
        data={
            "username": "testuser",
            "password": "wrongpassword",
        },
    )
    assert response.status_code == 401

    response_data = response.json()

    assert response_data["detail"] == "ユーザー名またはパスワードが正しくありません"


# 会議室
def test_create_room_without_authentication(client):
    """JWTなしで会議室作成に失敗するテスト"""
    response = client.post(
        "/rooms/",
        json={
            "room_name": "testroom",
            "capacity": 10,
        },
    )
    assert response.status_code == 401


def test_create_room(client, auth_headers):
    """JWTありで会議室作成に成功するテスト"""
    response = client.post(
        "/rooms/",
        headers=auth_headers,
        json={
            "room_name": "testroom",
            "capacity": 10,
        },
    )

    assert response.status_code == 201

    response_data = response.json()

    assert response_data["room_name"] == "testroom"
    assert response_data["capacity"] == 10
    assert "id" in response_data


def test_read_rooms(client, test_room):
    """会議室一覧を取得できるテスト"""
    response = client.get(
        "/rooms/",
    )

    assert response.status_code == 200

    response_data = response.json()

    assert len(response_data) == 1
    assert response_data[0]["id"] == test_room["id"]
    assert response_data[0]["room_name"] == test_room["room_name"]
    assert response_data[0]["capacity"] == 10


def test_read_room(client, test_room):
    """IDで会議室を1件取得できるテスト"""
    response = client.get(
        f"/rooms/{test_room['id']}",
    )

    assert response.status_code == 200

    response_data = response.json()

    assert response_data["id"] == test_room["id"]
    assert response_data["room_name"] == test_room["room_name"]
    assert response_data["capacity"] == 10


def test_read_room_not_found(client):
    """存在しない会議室の取得に失敗するテスト"""
    response = client.get("/rooms/999")

    assert response.status_code == 404

    response_data = response.json()

    assert response_data["detail"] == "会議室情報が見つかりません"


def test_update_room(client, auth_headers, test_room):
    """会議室を更新するテスト"""
    response = client.put(
        f"/rooms/{test_room['id']}",
        headers=auth_headers,
        json={
            "room_name": "updatedroom",
            "capacity": 20,
        },
    )
    assert response.status_code == 200

    response_data = response.json()

    assert response_data["id"] == test_room["id"]
    assert response_data["room_name"] == "updatedroom"
    assert response_data["capacity"] == 20


def test_update_room_not_found(client, auth_headers):
    """存在しない会議室の更新に失敗するテスト"""
    response = client.put(
        "/rooms/999",
        headers=auth_headers,
        json={
            "room_name": "updatedroom",
            "capacity": 20,
        },
    )
    assert response.status_code == 404

    response_data = response.json()

    assert response_data["detail"] == "会議室情報が見つかりません"


def test_update_room_no_authority(client, auth_headers, other_test_room):
    """他人の会議室の更新に失敗するテスト"""
    response = client.put(
        f"/rooms/{other_test_room['id']}",
        headers=auth_headers,
        json={
            "room_name": "updatedroom",
            "capacity": 20,
        },
    )
    assert response.status_code == 403

    response_data = response.json()
    assert response_data["detail"] == "この操作を行う権限がありません"


def test_delete_room(client, auth_headers, test_room):
    """本人が会議室を削除できるテスト"""
    room_id = test_room["id"]
    response = client.delete(
        f"/rooms/{room_id}",
        headers=auth_headers,
    )
    assert response.status_code == 204

    get_response = client.get(f"/rooms/{room_id}")

    assert get_response.status_code == 404


def test_delete_room_not_found(client, auth_headers):
    """存在しない会議室の削除に失敗するテスト"""
    response = client.delete(
        "/rooms/999",
        headers=auth_headers,
    )
    assert response.status_code == 404

    response_data = response.json()

    assert response_data["detail"] == "会議室情報が見つかりません"


def test_delete_room_no_authority(
    client,
    auth_headers,
    other_test_room,
):
    """他人の会議室の削除に失敗するテスト"""
    response = client.delete(
        f"/rooms/{other_test_room['id']}",
        headers=auth_headers,
    )
    assert response.status_code == 403

    response_data = response.json()

    assert response_data["detail"] == "この操作を行う権限がありません"


def test_delete_room_with_booking(client, auth_headers, test_booking):
    """予約がある会議室の削除に失敗するテスト"""
    response = client.delete(
        f"/rooms/{test_booking['room_id']}",
        headers=auth_headers,
    )
    assert response.status_code == 409

    response_data = response.json()
    assert response_data["detail"] == "この会議室には予約が存在するため削除できません"


# 予約
def test_create_booking_without_authentication(client):
    """JWTなしで予約作成に失敗するテスト"""
    response = client.post(
        "/bookings/",
        json={
            "room_id": 1,
            "start_at": "2026-08-02T10:00:00",
            "end_at": "2026-08-02T11:00:00",
            "reserved_num": 3,
        },
    )

    assert response.status_code == 401


def test_create_booking(client, auth_headers, test_room):
    """JWTありで予約作成に成功するテスト"""
    response = client.post(
        "/bookings/",
        headers=auth_headers,
        json={
            "room_id": test_room["id"],
            "start_at": "2026-08-02T10:00:00",
            "end_at": "2026-08-02T11:00:00",
            "reserved_num": 3,
        },
    )

    assert response.status_code == 201

    response_data = response.json()

    assert "id" in response_data
    assert response_data["room_id"] == test_room["id"]
    assert response_data["reserved_num"] == 3


def test_create_booking_conflict(
    client,
    auth_headers,
    test_booking,
):
    """既存予約と時間が重なる予約作成に失敗するテスト"""
    response = client.post(
        "/bookings/",
        headers=auth_headers,
        json={
            "room_id": test_booking["room_id"],
            "start_at": "2026-08-02T10:30:00",
            "end_at": "2026-08-02T11:30:00",
            "reserved_num": 2,
        },
    )

    assert response.status_code == 409

    response_data = response.json()

    assert "detail" in response_data


def test_read_bookings(
    client,
    auth_headers,
    test_booking,
):
    """認証済みユーザーが予約一覧を取得できるテスト"""
    response = client.get(
        "/bookings/",
        headers=auth_headers,
    )

    assert response.status_code == 200

    response_data = response.json()

    assert len(response_data) == 1
    assert response_data[0]["id"] == test_booking["id"]
    assert response_data[0]["room_id"] == test_booking["room_id"]
    assert response_data[0]["reserved_num"] == test_booking["reserved_num"]


def test_read_bookings_without_authentication(client):
    """JWTなしで予約一覧取得に失敗するテスト"""
    response = client.get("/bookings/")

    assert response.status_code == 401


def test_read_booking(
    client,
    auth_headers,
    test_booking,
):
    """IDを指定して予約を1件取得できるテスト"""
    response = client.get(
        f"/bookings/{test_booking['id']}",
        headers=auth_headers,
    )

    assert response.status_code == 200

    response_data = response.json()

    assert response_data["id"] == test_booking["id"]
    assert response_data["room_id"] == test_booking["room_id"]
    assert response_data["reserved_num"] == test_booking["reserved_num"]


def test_read_booking_not_found(client, auth_headers):
    """存在しない予約の取得に失敗するテスト"""
    response = client.get(
        "/bookings/999",
        headers=auth_headers,
    )

    assert response.status_code == 404

    response_data = response.json()

    assert response_data["detail"] == "予約情報が見つかりません"


def test_read_booking_without_authentication(client):
    """JWTなしで予約1件取得に失敗するテスト"""
    response = client.get("/bookings/999")

    assert response.status_code == 401


def test_update_booking(
    client,
    auth_headers,
    test_booking,
):
    """本人が予約を更新できるテスト"""
    response = client.put(
        f"/bookings/{test_booking['id']}",
        headers=auth_headers,
        json={
            "room_id": test_booking["room_id"],
            "start_at": "2026-08-02T14:00:00",
            "end_at": "2026-08-02T15:00:00",
            "reserved_num": 5,
        },
    )

    assert response.status_code == 200

    response_data = response.json()

    assert response_data["id"] == test_booking["id"]
    assert response_data["room_id"] == test_booking["room_id"]
    assert response_data["reserved_num"] == 5


def test_update_booking_not_found(
    client,
    auth_headers,
    test_room,
):
    """存在しない予約の更新に失敗するテスト"""
    response = client.put(
        "/bookings/999",
        headers=auth_headers,
        json={
            "room_id": test_room["id"],
            "start_at": "2026-08-02T14:00:00",
            "end_at": "2026-08-02T15:00:00",
            "reserved_num": 5,
        },
    )

    assert response.status_code == 404

    response_data = response.json()

    assert response_data["detail"] == "予約情報が見つかりません"


def test_update_booking_no_authority(
    client,
    auth_headers,
    other_test_booking,
):
    """他人の予約の更新に失敗するテスト"""
    response = client.put(
        f"/bookings/{other_test_booking['id']}",
        headers=auth_headers,
        json={
            "room_id": other_test_booking["room_id"],
            "start_at": "2026-08-02T14:00:00",
            "end_at": "2026-08-02T15:00:00",
            "reserved_num": 5,
        },
    )

    assert response.status_code == 403

    response_data = response.json()

    assert response_data["detail"] == ("この操作を行う権限がありません")


def test_update_booking_conflict(
    client,
    auth_headers,
    test_booking,
    second_test_booking,
):
    """既存予約と重なる時間帯への更新に失敗するテスト"""
    response = client.put(
        f"/bookings/{second_test_booking['id']}",
        headers=auth_headers,
        json={
            "room_id": test_booking["room_id"],
            "start_at": "2026-08-02T10:30:00",
            "end_at": "2026-08-02T11:30:00",
            "reserved_num": 2,
        },
    )

    assert response.status_code == 409

    response_data = response.json()

    assert "detail" in response_data


def test_delete_booking(
    client,
    auth_headers,
    test_booking,
):
    """本人が予約を削除できるテスト"""
    booking_id = test_booking["id"]

    response = client.delete(
        f"/bookings/{booking_id}",
        headers=auth_headers,
    )

    assert response.status_code == 204

    get_response = client.get(
        f"/bookings/{booking_id}",
        headers=auth_headers,
    )

    assert get_response.status_code == 404


def test_delete_booking_not_found(client, auth_headers):
    """存在しない予約の削除に失敗するテスト"""
    response = client.delete(
        "/bookings/999",
        headers=auth_headers,
    )

    assert response.status_code == 404

    response_data = response.json()

    assert response_data["detail"] == "予約情報が見つかりません"


def test_delete_booking_no_authority(
    client,
    auth_headers,
    other_test_booking,
):
    """他人の予約の削除に失敗するテスト"""
    response = client.delete(
        f"/bookings/{other_test_booking['id']}",
        headers=auth_headers,
    )

    assert response.status_code == 403

    response_data = response.json()

    assert response_data["detail"] == ("この操作を行う権限がありません")


def test_delete_booking_without_authentication(
    client,
    test_booking,
):
    """JWTなしで予約削除に失敗するテスト"""
    response = client.delete(
        f"/bookings/{test_booking['id']}",
    )

    assert response.status_code == 401
