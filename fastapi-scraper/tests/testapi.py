from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_upload_csv():
    response = client.post("/upload", files={"file": ("test.csv", "https://example.com\nhttps://test.com")})
    assert response.status_code == 200
    assert "task_ids" in response.json()

def test_status_check():
    response = client.get("/status/test_task_id")
    assert response.status_code == 200
    assert "status" in response.json()

def test_get_results():
    response = client.get("/results/test_task_id")
    assert response.status_code == 200
