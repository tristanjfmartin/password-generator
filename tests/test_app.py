import pytest
from app import app as flask_app


@pytest.fixture
def client():
    flask_app.config["TESTING"] = True
    with flask_app.test_client() as client:
        yield client


def test_home_returns_200(client):
    response = client.get("/")
    assert response.status_code == 200


def test_generate_returns_password_of_correct_length(client):
    response = client.post("/generate", json={
        "length": 16,
        "use_upper": True,
        "use_digits": True,
        "use_symbols": True,
    })
    assert response.status_code == 200
    data = response.get_json()
    assert "password" in data
    assert len(data["password"]) == 16


def test_generate_defaults_are_applied(client):
    response = client.post("/generate", json={"length": 12})
    assert response.status_code == 200
    password = response.get_json()["password"]
    assert len(password) == 12
    assert not password.islower()


def test_generate_rejects_length_too_short(client):
    response = client.post("/generate", json={"length": 4})
    assert response.status_code == 400
    assert "error" in response.get_json()


def test_generate_rejects_length_too_long(client):
    response = client.post("/generate", json={"length": 100})
    assert response.status_code == 400
    assert "error" in response.get_json()


def test_generate_lowercase_only_when_all_off(client):
    response = client.post("/generate", json={
        "length": 20,
        "use_upper": False,
        "use_digits": False,
        "use_symbols": False,
    })
    assert response.status_code == 200
    password = response.get_json()["password"]
    assert len(password) == 20
    assert all(c.islower() for c in password)


def test_generate_rejects_boolean_length(client):
    response = client.post("/generate", json={"length": True})
    assert response.status_code == 400
    assert "error" in response.get_json()


# --- Passphrase tests ---

def test_generate_passphrase_correct_word_count():
    from password_gen import generate_passphrase
    result = generate_passphrase(4)
    assert len(result.split("-")) == 4


def test_generate_passphrase_uses_hyphens():
    from password_gen import generate_passphrase
    result = generate_passphrase(3)
    assert result.count("-") == 2


def test_generate_passphrase_words_from_list():
    from password_gen import generate_passphrase
    from words import WORD_LIST
    result = generate_passphrase(5)
    for word in result.split("-"):
        assert word in WORD_LIST
