import urllib.parse


def test_get_activities_returns_activity_list(client):
    # Arrange
    activity_name = "Chess Club"

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    activities = response.json()
    assert activity_name in activities
    assert isinstance(activities[activity_name]["participants"], list)
    assert activities[activity_name]["description"] == "Learn strategies and compete in chess tournaments"


def test_signup_for_activity_adds_participant(client):
    # Arrange
    activity_name = "Chess Club"
    encoded_activity = urllib.parse.quote(activity_name, safe="")
    new_email = "test_student@mergington.edu"

    # Act
    response = client.post(
        f"/activities/{encoded_activity}/signup",
        params={"email": new_email},
    )

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": f"Signed up {new_email} for {activity_name}"}

    get_response = client.get("/activities")
    assert new_email in get_response.json()[activity_name]["participants"]


def test_duplicate_signup_returns_bad_request(client):
    # Arrange
    activity_name = "Chess Club"
    encoded_activity = urllib.parse.quote(activity_name, safe="")
    email = "duplicate_student@mergington.edu"

    # Act
    first_response = client.post(
        f"/activities/{encoded_activity}/signup",
        params={"email": email},
    )
    second_response = client.post(
        f"/activities/{encoded_activity}/signup",
        params={"email": email},
    )

    # Assert
    assert first_response.status_code == 200
    assert second_response.status_code == 400
    assert second_response.json()["detail"] == "Student already signed up"


def test_remove_participant_unregisters_student(client):
    # Arrange
    activity_name = "Chess Club"
    encoded_activity = urllib.parse.quote(activity_name, safe="")
    participant_email = "daniel@mergington.edu"

    # Act
    response = client.delete(
        f"/activities/{encoded_activity}/participants",
        params={"email": participant_email},
    )

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": f"Removed {participant_email} from {activity_name}"}

    get_response = client.get("/activities")
    assert participant_email not in get_response.json()[activity_name]["participants"]


def test_remove_nonexistent_participant_returns_not_found(client):
    # Arrange
    activity_name = "Chess Club"
    encoded_activity = urllib.parse.quote(activity_name, safe="")
    participant_email = "ghost_student@mergington.edu"

    # Act
    response = client.delete(
        f"/activities/{encoded_activity}/participants",
        params={"email": participant_email},
    )

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found"
