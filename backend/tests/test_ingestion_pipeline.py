import json
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def load_sample():
    with open("tests/sample_request.json") as f:
        return json.load(f)

def test_full_pipeline():
    payload = load_sample()

    # Validate
    res = client.post("/v1/json-request/validate", json=payload)
    assert res.status_code == 200

    # Normalize
    res = client.post("/v1/json-request/normalize", json=payload)
    assert res.status_code == 200

    # Save
    res = client.post("/v1/json-request/save", json=payload)
    assert res.status_code == 200
    request_id = res.json()["request_db_id"]

    # Send
    res = client.post(f"/v1/json-request/{request_id}/send")
    assert res.status_code == 200

    # Get
    res = client.get(f"/v1/json-request/{request_id}")
    assert res.status_code == 200

    # Logs
    res = client.get(f"/v1/json-request/{request_id}/logs")
    assert res.status_code == 200