from app import app


def test_index_returns_200():
    client = app.test_client()
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.get_json()


def test_healthz_returns_ok():
    client = app.test_client()
    response = client.get("/healthz")
    assert response.status_code == 200
    assert response.get_json()["status"] == "ok"
