def test_invalid_endpoint(client):
    response = client.get("/endpoint/that/does/not/exists")
    assert response.status_code == 404
    assert response.json() == {"detail": "Not Found"}
