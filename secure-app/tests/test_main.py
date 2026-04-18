from app.main import create_app


def test_health_endpoint() -> None:
    app = create_app()
    client = app.test_client()

    response = client.get("/health")

    assert response.status_code == 200
    assert response.get_json() == {"status": "ok"}


def test_echo_valid_message() -> None:
    app = create_app()
    client = app.test_client()

    response = client.post("/api/v1/echo", json={"message": "  hello secure world  "})

    assert response.status_code == 200
    assert response.get_json() == {"echo": "hello secure world"}


def test_echo_requires_json_object() -> None:
    app = create_app()
    client = app.test_client()

    response = client.post("/api/v1/echo", data="raw text", content_type="text/plain")

    assert response.status_code == 400
    assert response.get_json() == {"error": "JSON object body is required"}


def test_echo_requires_string_message() -> None:
    app = create_app()
    client = app.test_client()

    response = client.post("/api/v1/echo", json={"message": 42})

    assert response.status_code == 400
    assert response.get_json() == {"error": "'message' must be a string"}


def test_echo_rejects_empty_message() -> None:
    app = create_app()
    client = app.test_client()

    response = client.post("/api/v1/echo", json={"message": "   "})

    assert response.status_code == 400
    assert response.get_json() == {"error": "'message' cannot be empty"}


def test_echo_rejects_too_long_message() -> None:
    app = create_app()
    client = app.test_client()

    response = client.post("/api/v1/echo", json={"message": "a" * 201})

    assert response.status_code == 400
    assert response.get_json() == {"error": "'message' cannot exceed 200 characters"}


def test_echo_rejects_control_characters() -> None:
    app = create_app()
    client = app.test_client()

    response = client.post("/api/v1/echo", json={"message": "hello\nworld"})

    assert response.status_code == 400
    assert response.get_json() == {"error": "'message' contains invalid characters"}
