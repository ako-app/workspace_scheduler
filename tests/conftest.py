import pytest
from fastapi.testclient import TestClient

from backend.database import Base, get_db
from backend.main import app
from tests.database import override_get_db, testing_engine

app.dependency_overrides[get_db] = override_get_db


@pytest.fixture
def client():
    """テストDB・TestClient fixture"""
    Base.metadata.create_all(bind=testing_engine)

    try:
        with TestClient(app) as test_client:
            yield test_client
    finally:
        Base.metadata.drop_all(bind=testing_engine)


# テスト用ユーザー
@pytest.fixture
def test_user(client):
    response = client.post(
        "/users/",
        json={
            "username": "testuser",
            "password": "password123",
        },
    )
    assert response.status_code == 201
    return response.json()


# 認証済みユーザーのJWTヘッダー
@pytest.fixture
def auth_headers(client, test_user):
    response = client.post(
        "/auth/login",
        data={
            "username": "testuser",
            "password": "password123",
        },
    )
    assert response.status_code == 200
    access_token = response.json()["access_token"]

    return {"Authorization": f"Bearer {access_token}"}


# テスト用会議室
@pytest.fixture
def test_room(client, auth_headers):
    response = client.post(
        "/rooms/",
        headers=auth_headers,
        json={
            "room_name": "testroom",
            "capacity": 10,
        },
    )

    assert response.status_code == 201

    return response.json()


# テスト用予約
@pytest.fixture
def test_booking(client, auth_headers, test_room):
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

    return response.json()


@pytest.fixture
def other_user(client):
    """他のユーザー"""
    response = client.post(
        "/users/",
        json={
            "username": "otheruser",
            "password": "password123",
        },
    )

    assert response.status_code == 201
    return response.json()


@pytest.fixture
def other_auth_headers(client, other_user):
    """他人の認証"""
    response = client.post(
        "/auth/login",
        data={
            "username": "otheruser",
            "password": "password123",
        },
    )
    assert response.status_code == 200
    access_token = response.json()["access_token"]
    return {"Authorization": f"Bearer {access_token}"}


@pytest.fixture
def other_test_room(client, other_auth_headers):
    """他人のテスト会議室"""
    response = client.post(
        "/rooms/",
        headers=other_auth_headers,
        json={
            "room_name": "otherroom",
            "capacity": 5,
        },
    )

    assert response.status_code == 201
    return response.json()


@pytest.fixture
def other_test_booking(
    client,
    other_auth_headers,
    test_room,
):
    """別ユーザーが作成した予約データを返すfixture"""
    response = client.post(
        "/bookings/",
        headers=other_auth_headers,
        json={
            "room_id": test_room["id"],
            "start_at": "2026-08-02T12:00:00",
            "end_at": "2026-08-02T13:00:00",
            "reserved_num": 2,
        },
    )

    assert response.status_code == 201

    return response.json()


@pytest.fixture
def second_test_booking(
    client,
    auth_headers,
    test_room,
):
    """予約重複の更新テストに使う2件目の予約を返すfixture"""
    response = client.post(
        "/bookings/",
        headers=auth_headers,
        json={
            "room_id": test_room["id"],
            "start_at": "2026-08-02T12:00:00",
            "end_at": "2026-08-02T13:00:00",
            "reserved_num": 2,
        },
    )

    assert response.status_code == 201

    return response.json()
