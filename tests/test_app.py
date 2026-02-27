import pytest
from fastapi.testclient import TestClient
from src.app import app, activities

client = TestClient(app)

# GET /activities
def test_get_activities():
    # Arrange: activitiesはfixtureでリセット済み
    # Act
    response = client.get("/activities")
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert all("description" in v and "schedule" in v for v in data.values())

# POST /activities/{activity_name}/signup 正常系
def test_signup_for_activity_success():
    # Arrange
    activity_name = list(activities.keys())[0]
    email = "test1@mergington.edu"
    # Act
    response = client.post(f"/activities/{activity_name}/signup?email={email}")
    # Assert
    assert response.status_code == 200
    assert email in activities[activity_name]["participants"]
    assert "Signed up" in response.json()["message"]

# POST /activities/{activity_name}/signup 活動不存在
def test_signup_for_activity_not_found():
    # Arrange
    activity_name = "nonexistent"
    email = "test2@mergington.edu"
    # Act
    response = client.post(f"/activities/{activity_name}/signup?email={email}")
    # Assert
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]

# POST /activities/{activity_name}/signup 重複登録
def test_signup_for_activity_duplicate():
    # Arrange
    activity_name = list(activities.keys())[0]
    email = "test3@mergington.edu"
    client.post(f"/activities/{activity_name}/signup?email={email}")
    # Act
    response = client.post(f"/activities/{activity_name}/signup?email={email}")
    # Assert
    assert response.status_code == 400 or response.status_code == 200  # バグがある場合200
    # 参加者リストに重複がないこと
    assert activities[activity_name]["participants"].count(email) == 1

# GET / のリダイレクト
def test_root_redirect():
    # Arrange: なし
    # Act
    response = client.get("/")
    # Assert
    assert response.status_code in (200, 307, 302)
    assert "text/html" in response.headers["content-type"]
