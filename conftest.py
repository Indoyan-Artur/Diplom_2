import pytest
import requests
import random

URL = "https://stellarburgers.education-services.ru"
DISPOSABLE_PASSWORD = "Password123!"
NAME = "test user"


@pytest.fixture()
def user_creation():
    email = f"test-{random.randint(10000000, 99999999)}@yandex.ru"
    data = {"email": email, "password": DISPOSABLE_PASSWORD, "name": NAME}
    response = requests.post(f"{URL}/api/auth/register", json=data)

    assert response.status_code == 200, f"Регистрация не прошла: {response.status_code} {response.text}"

    login = requests.post(f"{URL}/api/auth/login", json={"email": email, "password": DISPOSABLE_PASSWORD})
    token = _token(login.json()) if login.ok else ""
    yield {"response": response, "credentials": data, "email": email, "token": token}
    if token:
        requests.delete(f"{URL}/api/auth/user", headers={"Authorization": f"Bearer {token}"})


def _token(login_data):
    token = (
        login_data.get("token")
        or login_data.get("access_token")
        or login_data.get("accessToken"))
    if token:
            token = token.removeprefix("Bearer ").strip()
    return token

@pytest.fixture()
def user_token(user_creation):
    creds = user_creation["credentials"]
    data = requests.post(f"{URL}/api/auth/login", json={"email": creds["email"], "password": creds["password"]}).json()
    token = _token(data)
    assert token, f"Токен не найден в ответе: {data}"
    return token

@pytest.fixture()
def authorization(user_creation):

    response = requests.post(f'{URL}/api/auth/login', json={"email": user_creation["email"], "password": DISPOSABLE_PASSWORD})
    token = response.json().get("accessToken", "")
    return {"response": response, "token": token}


@pytest.fixture()
def ingredient_ids():
    catalog = requests.get(f"{URL}/api/ingredients")
    assert catalog.status_code == 200, f"Каталог недоступен: {catalog.status_code} {catalog.text}"
    items = catalog.json()["data"]
    assert items, "Каталог пуст"
    
    return [item["_id"] for item in items[:2]]