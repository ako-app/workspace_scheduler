import pytest
from fastapi.testclient import TestClient

from backend.database import Base, get_db
from backend.main import app
from tests.database import override_get_db, testing_engine

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture
def client():
    Base.metadata.create_all(bind=testing_engine)

    with TestClient(app) as test_client:
        yield test_client

    Base.metadata.drop_all(bind=testing_engine)
    
    