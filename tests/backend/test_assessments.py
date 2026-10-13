import pytest

def test_mcq_grading(client, test_user_token, test_assessment):
    response = client.post(f"/api/assessments/{test_assessment.id}/submit", json={
        "answers": {
            "q1": "c1_2" # Correct choice id
        }
    }, headers={"Authorization": f"Bearer {test_user_token}"})
    assert response.status_code == 200
    assert response.json()["score"] == 1.0

def test_coding_challenge_grading(client, test_user_token):
    # Mocking coding challenge submission
    response = client.post("/api/assessments/code/submit", json={
        "challenge_id": 1,
        "code": "def solve(): return True"
    }, headers={"Authorization": f"Bearer {test_user_token}"})
    assert response.status_code in [200, 202]

def test_submission_recording(client, test_user_token, test_assessment):
    # Submit
    client.post(f"/api/assessments/{test_assessment.id}/submit", json={"answers": {}}, headers={"Authorization": f"Bearer {test_user_token}"})
    
    # Check progress
    response = client.get("/api/progress", headers={"Authorization": f"Bearer {test_user_token}"})
    assert response.status_code == 200
    progress = response.json()
    assert len(progress) > 0
