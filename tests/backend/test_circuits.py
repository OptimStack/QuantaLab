import pytest

def test_create_circuit(client, test_user_token):
    response = client.post("/api/circuits", json={
        "name": "Test Circuit",
        "qasm": 'OPENQASM 2.0;\ninclude "qelib1.inc";\nqreg q[1];\nh q[0];'
    }, headers={"Authorization": f"Bearer {test_user_token}"})
    assert response.status_code == 200
    assert response.json()["name"] == "Test Circuit"

def test_get_circuits(client, test_user_token, test_circuit):
    response = client.get("/api/circuits", headers={"Authorization": f"Bearer {test_user_token}"})
    assert response.status_code == 200
    assert len(response.json()) > 0

def test_qasm_validation_max_qubits(client, test_user_token):
    # Assuming max qubits is 20
    qasm_str = 'OPENQASM 2.0;\ninclude "qelib1.inc";\nqreg q[25];\nh q[0];'
    response = client.post("/api/circuits/validate", json={"qasm": qasm_str}, headers={"Authorization": f"Bearer {test_user_token}"})
    assert response.status_code == 400
    assert "qubits" in response.json()["detail"].lower()
