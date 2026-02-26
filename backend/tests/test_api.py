from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
import pytest

from app.main import app
from app.db import Base, get_db

# Use an in-memory SQLite database for testing
SQLALCHEMY_DATABASE_URL = "sqlite://"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

def test_upload_log():
    raw_content = """#Game No : G123456789
#Table Name : Table Blue
#Game Type : No Limit Hold'em
#Stakes : $0.05/$0.10
Player 1 posts small blind $0.05
...
"""
    files = {"file": ("test_log.txt", raw_content)}
    response = client.post("/upload-log/", files=files)
    
    assert response.status_code == 200
    data = response.json()
    assert data["count"] == 1
    assert len(data["hand_ids"]) == 1

def test_read_hands():
    # Upload first
    raw_content = """#Game No : G123456789
#Table Name : Table Blue
#Game Type : No Limit Hold'em
#Stakes : $0.05/$0.10
Player 1 posts small blind $0.05
...
"""
    files = {"file": ("test_log.txt", raw_content)}
    client.post("/upload-log/", files=files)
    
    response = client.get("/hands/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["game_no"] == "G123456789"
