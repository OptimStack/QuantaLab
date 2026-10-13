import pytest
from app.core.security import verify_password, get_password_hash
# Assuming standard FastAPI test setup

def test_user_registration(client):
    response = client.post("/api/auth/register", json={
        "email": "test@example.com",
        "password": "strongpassword123",
        "full_name": "Test User"
    })
    # Assert depending on exact implementation, e.g. 201 or 200
    assert response.status_code in [200, 201]
    assert response.json()["email"] == "test@example.com"

def test_login_success(client, test_user):
    response = client.post("/api/auth/login", data={
        "username": test_user.email,
        "password": "testpassword"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"

def test_login_incorrect_credentials(client, test_user):
    response = client.post("/api/auth/login", data={
        "username": test_user.email,
        "password": "wrongpassword"
    })
    assert response.status_code == 401

def test_jwt_validation(client, test_user_token):
    response = client.get("/api/users/me", headers={"Authorization": f"Bearer {test_user_token}"})
    assert response.status_code == 200

def test_role_based_access(client, test_student_token):
    # Student trying to access admin endpoint
    response = client.get("/api/admin/stats", headers={"Authorization": f"Bearer {test_student_token}"})
    assert response.status_code == 403
