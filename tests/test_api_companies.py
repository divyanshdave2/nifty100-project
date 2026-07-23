def test_get_companies(client):
    response = client.get("/api/v1/companies")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_company_profile(client):
    # Test with a mock or default ticker
    response = client.get("/api/v1/companies/TCS")
    # Should either return 200 with data or 404 cleanly
    assert response.status_code in [200, 404]

def test_get_company_ratios(client):
    response = client.get("/api/v1/companies/TCS/ratios")
    assert response.status_code == 200
    data = response.json()
    assert "ratios" in data