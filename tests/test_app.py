from conftest import login

def csrf(client):
    with client.session_transaction() as sess:
        sess["_csrf_token"] = "test-token"
    return "test-token"

def test_login_and_dashboard(client):
    response = login(client)
    assert response.status_code == 200
    assert "Painel de acompanhamento".encode() in response.data

def test_vehicle_registration_and_maintenance(client):
    login(client)
    token = csrf(client)
    response = client.post("/vehicles/new", data={
        "_csrf_token": token, "plate": "ABC1D23", "model": "Fiat Uno",
        "year": "2015", "asset_number": "PAT-001"
    }, follow_redirects=True)
    assert response.status_code == 200
    assert "Veículo cadastrado com sucesso".encode() in response.data

    with client.application.app_context():
        from app import get_db
        vehicle = get_db().execute("SELECT id FROM vehicles WHERE plate = 'ABC1D23'").fetchone()

    response = client.post("/maintenances/new", data={
        "_csrf_token": token, "vehicle_id": str(vehicle["id"]),
        "description": "Revisão do sistema de freios",
        "request_date": "2026-11-12"
    }, follow_redirects=True)
    assert response.status_code == 200
    assert "Solicitação registrada com sucesso".encode() in response.data

def test_protected_page_redirects(client):
    response = client.get("/dashboard")
    assert response.status_code == 302
    assert "/login" in response.location
