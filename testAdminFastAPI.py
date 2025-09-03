# test_main.py
from fastapi.testclient import TestClient
from adminAPIFast import app  # Import your FastAPI app

client = TestClient(app)

def test_create_assistant():
    response = client.post(
        "/create_or_update_assistant",
        data={
            "id": "123",
            "type": "MyType",
            "description": "Test description",
            "action": "create"
        }
    )
    assert response.status_code == 200
    print(response.json())  # See the actual result
