def test_screener_valid(client):
    response = client.get("/api/v1/screener?min_roe=15.0&max_de=1.0")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_screener_invalid_params(client):
    response = client.get("/api/v1/screener?min_roe=-10")
    assert response.status_code == 400