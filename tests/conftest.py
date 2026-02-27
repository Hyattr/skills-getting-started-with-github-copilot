import pytest
from src import app

@pytest.fixture(autouse=True)
def reset_activities(monkeypatch):
    # Arrange: activitiesを初期化
    from src.app import activities
    for k in activities:
        activities[k]["participants"] = []
    yield
    # テスト後もリセット
    for k in activities:
        activities[k]["participants"] = []
